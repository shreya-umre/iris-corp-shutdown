# Data Quality & Ingestion Summary Report
**Assignment ID:** `IRIS-CORP-SHUTDOWN`  
**Target Schema:** `iris_staging.corporate_distress_records`  
**Execution Timestamp:** 2026-10-29T16:15:00Z  

---

## 1. Executive Summary
The `IRIS-CORP-SHUTDOWN` ingestion pipeline was executed against 17 synthetic administrative notice fixtures modeled on official German state gazettes, municipal portals (e.g., UVP-Verbund, Thru.de), and BImSchG legal templates.

* **Total Fixtures Processed:** 17
* **Successfully Validated & Staged Records:** 14 (Includes core signals and negative controls)
* **Quarantined / Rejected Records:** 3 (Caught during validation checks)
* **Pipeline Error Rate:** 17.6% (Intentionally engineered malformed edge cases)

---

## 2. Signal Separation Metrics

The pipeline accurately categorized notices into distinct distress signals using legal basis mappings (§§ 10, 15, 18, 20, 21 BImSchG) and contextual NLP logic:

| Signal Category | Classification Logic | Count | Example Legal Basis |
| :--- | :--- | :---: | :--- |
| `CONFIRMED_CLOSURE` | Permanent revocations, closures, or erloschen notices | 6 | § 21 BImSchG, § 20 BImSchG, § 18 BImSchG |
| `POTENTIAL_SHUTDOWN` | Advance notifications or intent to cease operations | 2 | § 15 BImSchG (Abs. 3) |
| `NEGATIVE_CONTROL` | Routine modifications, water law permits, or retractions | 6 | § 16 BImSchG, WHG, Retractions |
| **Total Staged** | | **14** | |

---

## 3. Data Quality & Quarantined Records Log

The pipeline implements strict quality gates prior to staging. Records with fatal validation failures are quarantined into error logs rather than ingested into `iris_staging`.

### Quarantined Records Summary

| Fixture ID | Error Type | Cause / Description | Action Taken |
| :--- | :--- | :--- | :--- |
| `notice_11_bad_missing_date` | `Missing Event Date` | Field `Datum:` was blank or unparseable | Quarantined to Error Log |
| `notice_12_bad_missing_operator` | `Missing Operator` | Field `Betreiber:` was blank | Quarantined to Error Log |
| `notice_13_bad_impossible_date` | `Calendar Range Error` | Invalid calendar date (`31.02.2025`) | Quarantined to Error Log |

### Handled Edge Cases (Passed Data Quality Gates)
* **UTF-8 Mojibake Recovery (`notice_14_bad_mojibake`):** Successfully normalized encoding corruption (`MÃ¤rz` $\rightarrow$ `März`) and parsed valid event date `2025-03-14`.
* **Multi-Format Date Normalization:** Standardized ISO (`YYYY-MM-DD`), German short (`DD.MM.YYYY`), and full written German dates (`14. März 2025`) into unified `YYYY-MM-DD` string representations.
* **Retraction Handling (`notice_10_neg_control_retraction`):** Identified explicit retraction keywords ("Rücknahme") and successfully classified the notice as `NEGATIVE_CONTROL` to prevent false-positive distress alerting.

---

## 4. Staging Schema Validation Queries

To verify data integrity within `iris_staging.corporate_distress_records` after pipeline execution, the following SQL validation queries are provided for the review team:

### Query 1: Verify Breakdown of Staged Signals
```sql
SELECT 
    event_type, 
    COUNT(*) AS record_count
FROM iris_staging.corporate_distress_records
GROUP BY event_type
ORDER BY record_count DESC;
```

### Query 2: Identify High-Risk Confirmed Closures
```sql
SELECT 
    facility_name, 
    permitting_authority, 
    legal_basis, 
    event_date, 
    source_url
FROM iris_staging.corporate_distress_records
WHERE event_type = 'CONFIRMED_CLOSURE'
ORDER BY event_date DESC;
```

### Query 3: Check Data Completeness Thresholds
```sql
SELECT 
    COUNT(*) AS total_records,
    COUNT(facility_name) AS valid_operators,
    COUNT(event_date) AS valid_dates,
    COUNT(legal_basis) AS valid_legal_refs
FROM iris_staging.corporate_distress_records
WHERE facility_name IS NULL OR event_date IS NULL;
```