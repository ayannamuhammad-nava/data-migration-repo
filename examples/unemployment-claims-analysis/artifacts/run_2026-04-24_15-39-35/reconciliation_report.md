# Post-Migration Reconciliation Report: employers


## row_count — PASS

Severity: INFO | Penalty: 0.0

- **legacy_count**: 5

- **modern_count**: 5

- **match**: True

- **difference**: 0


## checksums — PASS

Severity: INFO | Penalty: 0

- **_summary**: {'total_columns': 0, 'matches': 0, 'mismatches': 0, 'match_rate': 0}


## referential_integrity — SKIP

Severity: INFO | Penalty: 0

- **reason**: No FK checks configured for employers


## sample_compare — ERROR

Severity: INFO | Penalty: 0

- **error**: column "er_recid" does not exist
LINE 1: SELECT * FROM employers WHERE er_recid IN (2, 1, 5, 3, 4)
                                      ^



## aggregates — SKIP

Severity: INFO | Penalty: 0

- **reason**: No aggregate checks configured for employers


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

