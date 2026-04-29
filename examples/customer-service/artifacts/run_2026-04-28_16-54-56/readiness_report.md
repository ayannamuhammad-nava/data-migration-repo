# Pre-Migration Readiness Report: contacts


## schema_diff — WARN

Severity: MEDIUM | Penalty: 10.0


## pandera_validation — PASS

Severity: INFO | Penalty: 0

- **errors**: []


## governance — WARN

Severity: MEDIUM | Penalty: 0

- **pii_columns**: ['ct_ssn', 'ct_dob']

- **naming_violations**: []

- **missing_required**: []

- **null_violations**: {}

- **governance_score**: 90.0


## profile_risk — PASS

Severity: INFO | Penalty: 0

- **risk_count**: 0

- **risks**: []

- **high_risks**: 0

- **medium_risks**: 0


## etl_tests — SKIP

Severity: INFO | Penalty: 0

- **reason**: No transform script found at /Users/ayannamuhammad/cobol-programming-course-main/unemployment-claims-analysis/lockpicks-data-migration/projects/customer-service/artifacts/generated_schema/contacts_transforms.sql


## data_quality — PASS

Severity: INFO | Penalty: 0

- **anomalies**: []

- **count**: 0
