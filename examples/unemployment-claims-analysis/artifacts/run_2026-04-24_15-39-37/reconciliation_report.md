# Post-Migration Reconciliation Report: benefit_payments


## row_count — FAIL

Severity: HIGH | Penalty: 30.0

- **legacy_count**: 20

- **modern_count**: 14

- **match**: False

- **difference**: 6


## checksums — PASS

Severity: INFO | Penalty: 0

- **_summary**: {'total_columns': 0, 'matches': 0, 'mismatches': 0, 'match_rate': 0}


## referential_integrity — SKIP

Severity: INFO | Penalty: 0

- **reason**: No FK checks configured for benefit_payments


## sample_compare — ERROR

Severity: INFO | Penalty: 0

- **error**: column benefit_payments.bp_recid does not exist
LINE 2: FROM benefit_payments WHERE benefit_payments.bp_recid IN (14...
                                    ^



## aggregates — SKIP

Severity: INFO | Penalty: 0

- **reason**: No aggregate checks configured for benefit_payments


## archived_leakage — PASS

Severity: INFO | Penalty: 0

- **violations**: []

- **violation_count**: 0


## unmapped_columns — ERROR

Severity: INFO | Penalty: 0

- **error**: current transaction is aborted, commands ignored until end of transaction block



## normalization_integrity — ERROR

Severity: HIGH | Penalty: 10

- **error**: Cannot access primary table benefit_payments: current transaction is aborted, commands ignored until end of transaction block



## encoding — ERROR

Severity: MEDIUM | Penalty: 0

- **error**: current transaction is aborted, commands ignored until end of transaction block

