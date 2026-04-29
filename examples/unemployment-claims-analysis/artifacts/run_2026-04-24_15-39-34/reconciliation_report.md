# Post-Migration Reconciliation Report: claimants


## row_count — FAIL

Severity: HIGH | Penalty: 10.0

- **legacy_count**: 10

- **modern_count**: 9

- **match**: False

- **difference**: 1


## checksums — PASS

Severity: INFO | Penalty: 0

- **_summary**: {'total_columns': 0, 'matches': 0, 'mismatches': 0, 'match_rate': 0}


## referential_integrity — SKIP

Severity: INFO | Penalty: 0

- **reason**: No FK checks configured for claimants


## sample_compare — ERROR

Severity: INFO | Penalty: 0

- **error**: column "cl_recid" does not exist
LINE 1: SELECT * FROM claimants WHERE cl_recid IN (10, 6, 7, 8, 1, 5...
                                      ^



## aggregates — SKIP

Severity: INFO | Penalty: 0

- **reason**: No aggregate checks configured for claimants


## archived_leakage — PASS

Severity: INFO | Penalty: 0

- **violations**: []

- **violation_count**: 0


## unmapped_columns — ERROR

Severity: INFO | Penalty: 0

- **error**: current transaction is aborted, commands ignored until end of transaction block



## normalization_integrity — SKIP

Severity: INFO | Penalty: 0

- **reason**: Not a normalized dataset


## encoding — ERROR

Severity: MEDIUM | Penalty: 0

- **error**: current transaction is aborted, commands ignored until end of transaction block

