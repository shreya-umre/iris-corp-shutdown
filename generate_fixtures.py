import os
import json

# Define directory structure
os.makedirs("fixtures/notices", exist_ok=True)
os.makedirs("fixtures/expected", exist_ok=True)

# Define all fixtures covering core cases, negative controls, and bad data
fixtures_data = [
    {
        "id": "notice_01_revocation",
        "format": "txt",
        "source_name": "Official Gazette Notice",
        "source_url": "https://example.invalid/bimschg/revocation-01",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://e-pflicht.ub.uni-duesseldorf.de/download/pdf/194193",
        "content": "Bekanntmachung über den Widerruf einer Immissionsschutzrechtlichen Genehmigung\nBehörde: Bezirksregierung Düsseldorf\nAktenzeichen: G 35/2025/012\nBetreiber: Rhein-Chemie Müller GmbH & Co. KG\nDatum: 14. März 2025\nBetreff: Vollständiger Widerruf der Genehmigung gemäß § 21 BImSchG nach dauerhafter Betriebseinstellung."
    },
    {
        "id": "notice_02_revocation_alt",
        "format": "txt",
        "source_name": "State Portal Notice",
        "source_url": "https://example.invalid/bimschg/revocation-02",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://e-pflicht.ub.uni-duesseldorf.de/download/pdf/194193",
        "content": "Widerrufsbescheid gemäß § 21 BImSchG\nBehörde: Landesamt für Natur, Umwelt und Verbraucherschutz NRW\nAktenzeichen: LANUV-883-2025\nBetreiber: Ruhr-Stahl AG\nDatum: 10.01.2025\nBetreff: Entzug der Betriebserlaubnis wegen Erlöschens der Voraussetzungen."
    },
    {
        "id": "notice_03_lapse_18",
        "format": "txt",
        "source_name": "Legal Status Bulletin",
        "source_url": "https://example.invalid/bimschg/lapse-03",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.gesetze-im-internet.de/bimschg/__18.html",
        "content": "Feststellung des Erlöschens\nBehörde: Regierungspräsidium Stuttgart\nAktenzeichen: 12-BImSchG-18\nBetreiber: Schwaben Metall GmbH\nDatum: 05.02.2025\nBetreff: Die Genehmigung ist nach § 18 BImSchG erloschen, da die Anlage seit über drei Jahren nicht mehr betrieben wurde."
    },
    {
        "id": "notice_04_waiver",
        "format": "txt",
        "source_name": "Court Reference Notice",
        "source_url": "https://example.invalid/bimschg/waiver-04",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://app.omnilex.ai/de/sources/court-decision/de-rii--wbre410019272/bverwg-2012-11-15-7-c-1512",
        "content": "Verzicht auf Genehmigung\nBehörde: Landkreis Leipzig Umweltamt\nAktenzeichen: L-ENV-2025-09\nBetreiber: Braunkohle AG\nDatum: 12.01.2025\nBetreff: Erklärung des Verzichts auf die immissionsschutzrechtliche Anlage."
    },
    {
        "id": "notice_05_prohibition_20",
        "format": "txt",
        "source_name": "Official Order Bulletin",
        "source_url": "https://example.invalid/bimschg/prohibition-05",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.uvp-verbund.de",
        "content": "Anordnung der Stilllegung\nBehörde: Bezirksregierung Köln\nAktenzeichen: K-20-2025\nBetreiber: Chemie-Park Rhein GmbH\nDatum: 18.02.2025\nBetreff: Stilllegungsanordnung gemäß § 20 BImSchG wegen schwerer Auflagenverstöße."
    },
    {
        "id": "notice_06_decom_15",
        "format": "txt",
        "source_name": "Municipal Environmental Notice",
        "source_url": "https://example.invalid/bimschg/decom-06",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.dresden.de/media/pdf/umwelt/Vdr86_020_Betriebseinstellung-BImSchG.pdf",
        "content": "Anzeige einer beabsichtigten Betriebseinstellung\nBehörde: Landeshauptstadt Dresden, Umweltamt\nAktenzeichen: 44-U-2026/88\nBetreiber: Elbe-Stahlwerke AG\nDatum: 14.03.2025\nBetreff: Anzeige der beabsichtigten Stilllegung der Gießerei gemäß § 15 Abs. 3 BImSchG."
    },
    {
        "id": "notice_07_decom_intent",
        "format": "txt",
        "source_name": "Municipal Portal Notice",
        "source_url": "https://example.invalid/bimschg/decom-07",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.dresden.de/media/pdf/umwelt/Vdr86_020_Betriebseinstellung-BImSchG.pdf",
        "content": "Mitteilung über geplante Maßnahmen\nBehörde: Stadt München\nAktenzeichen: M-15-2025\nBetreiber: Isar Tech GmbH\nDatum: 20.02.2025\nBetreff: Betreiber beabsichtigt die Stilllegung zum Jahresende nach § 15 BImSchG."
    },
    {
        "id": "notice_08_neg_control_approval",
        "format": "txt",
        "source_name": "District Government Announcement",
        "source_url": "https://example.invalid/bimschg/approval-08",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.bra.nrw.de/-5485",
        "content": "Öffentliche Bekanntmachung - Genehmigungsbescheid\nBehörde: Bezirksregierung Arnsberg\nAktenzeichen: 54-85/2026\nBetreiber: Westfalen Energie GmbH\nDatum: 2026-04-01\nBetreff: Änderungsgenehmigung nach § 16 BImSchG zur Errichtung einer Filteranlage. Keine Stilllegung."
    },
    {
        "id": "notice_09_neg_control_other",
        "format": "txt",
        "source_name": "Local Register",
        "source_url": "https://example.invalid/bimschg/other-09",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.bra.nrw.de/-5485",
        "content": "Wasserschutzrechtliche Erlaubnis\nBehörde: Landkreis München\nAktenzeichen: WS-99\nBetreiber: Aqua Service GmbH\nDatum: 10.01.2025\nBetreff: Erlaubnis nach Wasserhaushaltsgesetz (kein BImSchG)."
    },
    {
        "id": "notice_10_neg_control_retraction",
        "format": "txt",
        "source_name": "Correction Notice",
        "source_url": "https://example.invalid/bimschg/retraction-10",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://app.omnilex.ai",
        "content": "Rücknahme der Stilllegungsanzeige\nBehörde: Landeshauptstadt Dresden\nAktenzeichen: 44-U-2026/88\nBetreiber: Elbe-Stahlwerke AG\nDatum: 15.03.2025\nBetreff: Der Betreiber zieht die Stilllegungsanzeige nach § 15 BImSchG hiermit zurück."
    },
    {
        "id": "notice_11_bad_missing_date",
        "format": "txt",
        "source_name": "Faulty Notice",
        "source_url": "https://example.invalid/bimschg/bad-11",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.uvp-verbund.de",
        "content": "Widerruf der Genehmigung\nBehörde: Bezirksregierung Köln\nAktenzeichen: ERR-01\nBetreiber: Test Corp\nDatum: \nBetreff: Widerruf nach § 21 BImSchG ohne gültiges Datum."
    },
    {
        "id": "notice_12_bad_missing_operator",
        "format": "txt",
        "source_name": "Faulty Notice",
        "source_url": "https://example.invalid/bimschg/bad-12",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.uvp-verbund.de",
        "content": "Widerruf der Genehmigung\nBehörde: Bezirksregierung Köln\nAktenzeichen: ERR-02\nBetreiber: \nDatum: 2025-01-01\nBetreff: Widerruf nach § 21 BImSchG ohne Betreiberangabe."
    },
    {
        "id": "notice_13_bad_impossible_date",
        "format": "txt",
        "source_name": "Faulty Notice",
        "source_url": "https://example.invalid/bimschg/bad-13",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.uvp-verbund.de",
        "content": "Widerruf der Genehmigung\nBehörde: Bezirksregierung Köln\nAktenzeichen: ERR-03\nBetreiber: Invalid Date GmbH\nDatum: 31.02.2025\nBetreff: Widerruf nach § 21 BImSchG mit ungültigem Datum."
    },
    {
        "id": "notice_14_bad_mojibake",
        "format": "txt",
        "source_name": "Faulty Encoding Notice",
        "source_url": "https://example.invalid/bimschg/bad-14",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://e-pflicht.ub.uni-duesseldorf.de",
        "content": "Widerruf gemäß Â§ 21 BImSchG\nBehörde: Bezirksregierung DÃ¼sseldorf\nAktenzeichen: ERR-04\nBetreiber: MÃ¼ller & SÃ¶hne GmbH\nDatum: 14. MÃ¤rz 2025\nBetreff: Test mit falscher Kodierung."
    },
    {
        "id": "notice_15_duplicate_variant",
        "format": "txt",
        "source_name": "Variant Name Notice",
        "source_url": "https://example.invalid/bimschg/bad-15",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://e-pflicht.ub.uni-duesseldorf.de",
        "content": "Widerruf der Genehmigung\nBehörde: Bezirksregierung Düsseldorf\nAktenzeichen: G 35/2025/012\nBetreiber: Mueller GmbH und Co KG\nDatum: 14.03.2025\nBetreff: Vollständiger Widerruf nach § 21 BImSchG."
    },
    {
        "id": "notice_16_duplicate_source_a",
        "format": "txt",
        "source_name": "Authority Portal",
        "source_url": "https://example.invalid/bimschg/dup-A",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.uvp-verbund.de",
        "content": "Stilllegungsbescheid\nBehörde: Landkreis Harz\nAktenzeichen: HZ-2025-10\nBetreiber: Harz Calcium GmbH\nDatum: 2025-02-10\nBetreff: Widerruf nach § 21 BImSchG."
    },
    {
        "id": "notice_17_duplicate_source_uvp",
        "format": "txt",
        "source_name": "UVP Portal Mirror",
        "source_url": "https://example.invalid/bimschg/dup-UVP",
        "fetched_at": "2026-04-01T10:00:00Z",
        "inspired_by": "https://www.uvp-verbund.de/documents-ige-ng/igc_by/A2C552C3-E747-4F9C-9BA3-0BB5C5A84CC4/Bekanntmachung%20UVP%20Hartinger.doc",
        "content": "Stilllegungsbescheid\nBehörde: Landkreis Harz\nAktenzeichen: HZ-2025-10\nBetreiber: Harz Calcium GmbH\nDatum: 2025-02-10\nBetreff: Widerruf nach § 21 BImSchG."
    }
]

# Write out the notice files and build the manifest list
manifest_entries = []

for item in fixtures_data:
    file_path = f"fixtures/notices/{item['id']}.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(item["content"])
    
    entry = {
        "id": item["id"],
        "format": item["format"],
        "source_name": item["source_name"],
        "source_url": item["source_url"],
        "fetched_at": item["fetched_at"],
        "inspired_by": item["inspired_by"]
    }
    manifest_entries.append(entry)

manifest_data = {"fixtures": manifest_entries}
with open("fixtures/manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {len(fixtures_data)} notice fixtures and fixtures/manifest.json!")