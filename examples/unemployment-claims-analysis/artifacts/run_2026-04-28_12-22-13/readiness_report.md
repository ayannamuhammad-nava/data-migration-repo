# Pre-Migration Readiness Report: benefit_payments


## schema_diff — FAIL

Severity: HIGH | Penalty: 32.0

- **legacy_schema**: {'bp_recid': 'integer', 'bp_clmid': 'integer', 'bp_paydt': 'character', 'bp_payam': 'numeric', 'bp_methd': 'character', 'bp_wkedt': 'character', 'bp_stat': 'character', 'bp_chkno': 'character'}

- **mapping_types**: {'bp_recid': 'pending', 'bp_clmid': 'pending', 'bp_paydt': 'pending', 'bp_payam': 'pending', 'bp_methd': 'pending', 'bp_wkedt': 'pending', 'bp_stat': 'pending', 'bp_chkno': 'pending'}


## pandera_validation — PASS

Severity: INFO | Penalty: 0

- **errors**: []


## governance — WARN

Severity: MEDIUM | Penalty: 0

- **pii_columns**: []

- **naming_violations**: []

- **missing_required**: []

- **null_violations**: {'bp_chkno': np.float64(85.0)}

- **governance_score**: 97.0


## profile_risk — PASS

Severity: INFO | Penalty: 0

- **risk_count**: 0

- **risks**: []

- **high_risks**: 0

- **medium_risks**: 0


## etl_tests — PASS

Severity: INFO | Penalty: 0

- **issue_count**: 0

- **issues**: []

- **transform_path**: /Users/ayannamuhammad/cobol-programming-course-main/unemployment-claims-analysis/lockpicks-data-migration/projects/unemployment-claims-analysis/artifacts/generated_schema/benefit_payments_transforms.sql

- **mapping_count**: 8


## data_quality — PASS

Severity: INFO | Penalty: 0

- **anomalies**: []

- **count**: 0
