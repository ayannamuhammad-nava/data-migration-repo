# Post-Migration Reconciliation Report: claimants


## row_count — FAIL

Severity: HIGH | Penalty: 10.0

- **legacy_count**: 10

- **modern_count**: 9

- **match**: False

- **difference**: 1


## checksums — WARN

Severity: INFO | Penalty: 0

- **cl_recid->claimant_id**: {'legacy_checksum': '432f45b44c43...', 'modern_checksum': '4219afecb7d4...', 'match': False}

- **cl_fnam->first_name**: {'legacy_checksum': 'ed06e2f03344...', 'modern_checksum': '65ad8292138e...', 'match': False}

- **cl_lnam->last_name**: {'legacy_checksum': '5dfbdb740b99...', 'modern_checksum': '6f2e83047ab5...', 'match': False}

- **cl_phon->phone_number**: {'legacy_checksum': 'fb0c32120d7f...', 'modern_checksum': '119b0a764e9d...', 'match': False}

- **cl_emal->email**: {'legacy_checksum': '504b7674497d...', 'modern_checksum': '8e55bc15aa1d...', 'match': False}

- **cl_adr1->address_line1**: {'legacy_checksum': '41f62adaf2a1...', 'modern_checksum': '155bf6df3ed9...', 'match': False}

- **cl_city->city**: {'legacy_checksum': 'a3bd67951aa8...', 'modern_checksum': '963694d503d1...', 'match': False}

- **cl_st->state**: {'legacy_checksum': '46670ad40ed2...', 'modern_checksum': '1e5695ea3f95...', 'match': False}

- **cl_stat->claimant_status**: {'legacy_checksum': 'a4499a4b77ec...', 'modern_checksum': '351d808d5bc0...', 'match': False}

- **cl_rgdt->registered_at**: {'legacy_checksum': 'e95f43db6f14...', 'modern_checksum': '407610cee3a9...', 'match': False}

- **cl_dcsd->is_deceased**: {'legacy_checksum': 'ea33db10a76b...', 'modern_checksum': 'cacd3fb07138...', 'match': False}

- **_summary**: {'total_columns': 11, 'matches': 0, 'mismatches': 11, 'match_rate': 0.0}


## referential_integrity — SKIP

Severity: INFO | Penalty: 0

- **reason**: No FK checks configured for claimants


## sample_compare — FAIL

Severity: MEDIUM | Penalty: 3.3333333333333344

- **sample_size**: 9

- **exact_matches**: 8

- **discrepancies**: 1

- **match_rate**: 88.88888888888889

- **sample_discrepancies**: [{'id': 10, 'differences': [{'legacy_column': 'cl_stat', 'modern_column': 'claimant_status', 'legacy_value': 'ACTIVE              ', 'modern_value': 'inactive'}]}]


## aggregates — SKIP

Severity: INFO | Penalty: 0

- **reason**: No aggregate checks configured for claimants


## archived_leakage — FAIL

Severity: CRITICAL | Penalty: 20

- **violations**: [{'column': 'cl_bact', 'table': 'claimants', 'rationale': 'PII field cl_bact not present in modern schema — likely archived for compliance', 'severity': 'CRITICAL'}]

- **violation_count**: 1


## unmapped_columns — WARN

Severity: MEDIUM | Penalty: 5

- **ungoverned_columns**: ['legacy_system_ref']

- **count**: 1


## normalization_integrity — SKIP

Severity: INFO | Penalty: 0

- **reason**: Not a normalized dataset


## encoding — PASS

Severity: INFO | Penalty: 0

- **columns_checked**: 11

- **sample_size**: 1000

- **issue_count**: 0

- **issues**: []
