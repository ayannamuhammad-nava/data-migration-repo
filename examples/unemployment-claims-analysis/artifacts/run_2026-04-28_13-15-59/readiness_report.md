# Pre-Migration Readiness Report: employers


## schema_diff — PASS

Severity: LOW | Penalty: 0.0


## pandera_validation — PASS

Severity: INFO | Penalty: 0

- **errors**: []


## governance — PASS

Severity: INFO | Penalty: 0

- **pii_columns**: []

- **naming_violations**: []

- **missing_required**: []

- **null_violations**: {}

- **governance_score**: 100.0


## profile_risk — PASS

Severity: INFO | Penalty: 0

- **risk_count**: 0

- **risks**: []

- **high_risks**: 0

- **medium_risks**: 0


## etl_tests — WARN

Severity: MEDIUM | Penalty: 1

- **issue_count**: 1

- **issues**: [{'test': 'transform_source_missing', 'severity': 'MEDIUM', 'detail': 'Transform for er_zip->zip_code not found in script'}]

- **transform_path**: /Users/ayannamuhammad/cobol-programming-course-main/unemployment-claims-analysis/lockpicks-data-migration/projects/unemployment-claims-analysis/artifacts/generated_schema/employers_transforms.sql

- **mapping_count**: 10


## data_quality — PASS

Severity: INFO | Penalty: 0

- **anomalies**: []

- **count**: 0
