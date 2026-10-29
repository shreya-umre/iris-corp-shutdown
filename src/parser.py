import os
import json
import re
from datetime import datetime

def parse_date(date_str):
    """Parse ISO, German numeric, and German month-name dates."""
    if not date_str or not date_str.strip():
        raise ValueError("Missing event date")

    value = date_str.strip()

    # Try ISO format first.
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        pass

    # Normalize whitespace and case.
    value = re.sub(r"\s+", " ", value).lower()

    # Handle German month-name dates, e.g. 14. März 2025.
    months = {
        "januar": 1, "februar": 2, "märz": 3, "maerz": 3,
        "marz": 3, "april": 4, "mai": 5, "juni": 6,
        "juli": 7, "august": 8, "september": 9,
        "oktober": 10, "november": 11, "dezember": 12,
    }

    # Normalize common encoding errors and UTF-8 mojibake
    value = value.replace("mã¤rz", "märz")
    value = value.replace("mÃ¤rz", "märz")
    value = value.replace("mÃƒÂ¤rz", "märz")
    value = value.replace("maerz", "märz")

    match = re.fullmatch(
        r"(\d{1,2})\.?\s+([a-zäöü]+)\s+(\d{4})",
        value,
        flags=re.IGNORECASE,
    )

    if match:
        day, month_name, year = match.groups()
        month = months.get(month_name.lower())
        if month is not None:
            parsed = datetime(int(year), month, int(day))
            return parsed.strftime("%Y-%m-%d")

    # German numeric format: DD.MM.YYYY
    match = re.fullmatch(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", value)
    if match:
        day, month, year = match.groups()
        parsed = datetime(int(year), int(month), int(day))
        return parsed.strftime("%Y-%m-%d")

    raise ValueError(f"Unrecognized date format: {date_str!r}")


def classify_event(legal_basis, subject_text):
    """Classify notice into proper corporate distress signal categories."""
    text = (legal_basis + " " + subject_text).lower()
    
    # Retractions or negative controls
    if "rücknahme" in text or "änderungsgenehmigung" in text or "wasserhaushaltsgesetz" in text:
        return "NEGATIVE_CONTROL"
    
    # Confirmed closures / revocations (§ 21, § 20, § 18)
    if "§ 21" in text or "§ 20" in text or "§ 18" in text or "widerruf" in text or "erloschen" in text or "stilllegungsanordnung" in text:
        return "CONFIRMED_CLOSURE"
        
    # Potential shutdown notifications (§ 15)
    if "§ 15" in text or "beabsichtigt" in text or "geplante" in text:
        return "POTENTIAL_SHUTDOWN"
        
    return "NEGATIVE_CONTROL"

def process_notices(manifest_path=None):
    if manifest_path is None:
        # Check standard path or fallback to parent if run from tests/
        if os.path.exists("fixtures/manifest.json"):
            manifest_path = "fixtures/manifest.json"
        elif os.path.exists("../fixtures/manifest.json"):
            manifest_path = "../fixtures/manifest.json"
        else:
            manifest_path = "fixtures/manifest.json"

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    else:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        
    staging_records = []
    error_logs = []
    
    # Determine base path for notices depending on where script is executed from
    notices_dir = "fixtures/notices" if os.path.exists("fixtures/notices") else "../fixtures/notices"

    for fixture in manifest.get("fixtures", []):
        file_path = os.path.join(notices_dir, f"{fixture['id']}.txt")
        
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Fixture file missing: {file_path}")
                
            with open(file_path, "r", encoding="utf-8", errors="replace") as nf:
                content = nf.read()
                
            if not content.strip():
                raise ValueError("Empty notice file")
                
            # Extract fields safely using line-anchored regex
            auth_match = re.search(r"^Behörde:\s*(.*)$", content, re.MULTILINE)
            op_match = re.search(r"^Betreiber:\s*(.*)$", content, re.MULTILINE)
            date_match = re.search(r"^Datum:\s*(.*)$", content, re.MULTILINE)
            legal_match = re.search(r"(§\s*\d+(?:\s*Abs\.\s*\d+)?)", content)
            subject_match = re.search(r"^Betreff:\s*(.*)$", content, re.MULTILINE)
            
            authority = auth_match.group(1).strip() if auth_match else ""
            operator = op_match.group(1).strip() if op_match else ""
            raw_date = date_match.group(1).strip() if date_match else ""
            legal_basis = legal_match.group(1).strip() if legal_match else "Unknown"
            subject = subject_match.group(1).strip() if subject_match else content
            
            if not operator:
                raise ValueError("Missing facility/operator name")
                
            if not raw_date:
                raise ValueError("Missing event date")

            normalized_date = parse_date(raw_date)
            event_type = classify_event(legal_basis, subject)
            
            # Build staging record object
            record = {
                "record_id": f"sha256_{fixture['id']}",
                "facility_name": operator,
                "permitting_authority": authority,
                "legal_basis": legal_basis,
                "event_type": event_type,
                "event_date": normalized_date,
                "source_url": fixture["source_url"],
                "ingestion_timestamp": datetime.utcnow().isoformat() + "Z"
            }
            staging_records.append(record)
            
        except Exception as e:
            error_logs.append({
                "fixture_id": fixture["id"],
                "error": str(e)
            })
            
    return staging_records, error_logs

if __name__ == "__main__":
    records, errors = process_notices()
    print(f"Successfully processed {len(records)} records into staging schema.")
    print(f"Caught and quarantined {len(errors)} bad records during validation.")