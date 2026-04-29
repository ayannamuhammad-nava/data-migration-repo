# Pre-Migration Readiness Report: claimants


## schema_diff — WARN

Severity: MEDIUM | Penalty: 10.0


## pandera_validation — PASS

Severity: INFO | Penalty: 0

- **errors**: []


## governance — WARN

Severity: MEDIUM | Penalty: 0

- **pii_columns**: ['cl_ssn', 'cl_dob']

- **naming_violations**: []

- **missing_required**: []

- **null_violations**: {'cl_emal': np.float64(20.0)}

- **governance_score**: 87.0


## profile_risk — PASS

Severity: INFO | Penalty: 0

- **risk_count**: 0

- **risks**: []

- **high_risks**: 0

- **medium_risks**: 0


## etl_tests — WARN

Severity: MEDIUM | Penalty: 4

- **issue_count**: 3

- **transform_path**: /Users/ayannamuhammad/cobol-programming-course-main/unemployment-claims-analysis/lockpicks-data-migration/projects/unemployment-claims-analysis/artifacts/generated_schema/claimants_transforms.sql

- **mapping_count**: 17


## data_quality — PASS

Severity: INFO | Penalty: 0

- **anomalies**: []

- **count**: 0
