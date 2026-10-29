# IRIS Corporate Shutdown & Distress Intelligence Pipeline

**Assignment ID:** `IRIS-CORP-SHUTDOWN`  
**Assignment:** Large Industrial BImSchG Permit Revocation Alert

---

## 1. Overview
This pipeline automates the ingestion, parsing, normalization, and classification of industrial regulatory notices and state gazette announcements related to corporate facility shutdowns, revocations, and operational changes. It transforms unstructured or semi-structured administrative text into clean, standardized records mapped strictly to isolated staging schemas (`iris_staging.corporate_distress_records`), designed to feed corporate intelligence and risk dashboards without touching production cores (`iris_core`).

## 2. Project Architecture & File Structure
```text
iris-corp-shutdown/
│
├── fixtures/
│   ├── notices/              # 17 Raw text fixtures (gazettes, portal notices, edge cases)
│   └── manifest.json         # Provenance registry (source URLs, legal refs, metadata)
│
├── src/
│   └── parser.py             
│
├── tests/
│   └── test_parser.py        
│
├── Dockerfile                
├── data_quality_report.md    
└── README.md                 
```

## 3. Data Provenance & Handling Negative Controls
To reflect real-world BImSchG administrative data quality challenges, synthetic test fixtures were modeled directly after official German state gazettes (e.g., UVP-Verbund, Thru.de, Amtsblatt):
* **Core Signals:** Confirmed closures/revocations under § 21, § 20, and § 18 BImSchG (`CONFIRMED_CLOSURE`) and potential shutdown notices under § 15 BImSchG (`POTENTIAL_SHUTDOWN`).
* **Negative Controls:** Routine plant modification approvals (§ 16 BImSchG) and non-BImSchG water regulations, ensuring the parser filters out false positives (`NEGATIVE_CONTROL`).
* **Error Quarantining:** Malformed files (missing operators, empty dates, impossible calendar dates like Feb 31st, and UTF-8 Mojibake encoding anomalies such as `MÃ¤rz`) are caught and logged to error structures rather than crashing the pipeline.

For a full breakdown of quarantined edge cases, signal separation counts, and staging verification queries, see **`data_quality_report.md`**.

## 4. Run & Test Instructions

### Option A: Running Locally via Python
1. Install dependencies:
   ```bash
   pip install pytest
   ```
2. Run the test suite:
   ```bash
   pytest
   ```

### Option B: Running via Docker (Recommended for Reproducibility)
1. Build the Docker image from the project root:
   ```bash
   docker build -t iris-corp-shutdown .
   ```
2. Run the containerized test suite:
   ```bash
   docker run --rm iris-corp-shutdown
   ```

## 5. Summary of Limitations & Assumptions
* **Strict Database & Staging Isolation:** All output targets are strictly directed to `iris_staging.corporate_distress_records`. In accordance with system constraints, the pipeline never attempts writes or schema modifications to `iris_core` or live production database resources.
* **Deterministic Local Ingestion:** In production, state gazettes and regional environmental portals require active web scrapers. This submission decouples web scraping from parsing by utilizing a deterministic local landing zone (`fixtures/`) governed by `manifest.json` for evaluation reproducibility.
* **Header-Based Regex Extraction Scope:** The parser utilizes line-anchored regular expressions tailored to standard German administrative notification headers (`Behörde:`, `Betreiber:`, `Datum:`, `Betreff:`). In a live enterprise environment with multi-page OCR PDF inputs, a secondary layout-aware spatial extraction model (e.g., LayoutLM or LLM fallback) would complement this regular expressions parser.
