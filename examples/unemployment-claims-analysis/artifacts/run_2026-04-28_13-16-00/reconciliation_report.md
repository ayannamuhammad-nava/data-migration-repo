# Post-Migration Reconciliation Report: claims


## row_count — FAIL

Severity: HIGH | Penalty: 20.0

- **legacy_count**: 15

- **modern_count**: 12

- **match**: False

- **difference**: 3


## checksums — WARN

Severity: INFO | Penalty: 0

- **cm_recid->claim_id**: {'legacy_checksum': 'd92fe77e057d...', 'modern_checksum': 'dbf6db2c2cbd...', 'match': False}

- **cm_clmnt->claimant_id**: {'legacy_checksum': '64ac4d5903f4...', 'modern_checksum': 'fa6c9bd98627...', 'match': False}

- **cm_emplr->employer_id**: {'legacy_checksum': '9f00d8632d81...', 'modern_checksum': 'd42d2fd4aaf9...', 'match': False}

- **cm_seprs->separation_reason**: {'legacy_checksum': '9dd2e3e6f5af...', 'modern_checksum': 'cbd6db15c44b...', 'match': False}

- **cm_fildt->filing_date**: {'legacy_checksum': '560475fcda77...', 'modern_checksum': '4234bce44a7f...', 'match': False}

- **cm_bystr->benefit_year_start**: {'legacy_checksum': '560475fcda77...', 'modern_checksum': '4234bce44a7f...', 'match': False}

- **cm_byend->benefit_year_end**: {'legacy_checksum': '13cc32408f8d...', 'modern_checksum': '57a99ee4308c...', 'match': False}

- **cm_wkamt->weekly_benefit_amount**: {'legacy_checksum': '95a1751e3b38...', 'modern_checksum': '191088848a73...', 'match': False}

- **cm_mxamt->max_benefit_amount**: {'legacy_checksum': 'f42974c10776...', 'modern_checksum': '13d523ae308f...', 'match': False}

- **cm_totpd->total_paid**: {'legacy_checksum': '6471a1599d6a...', 'modern_checksum': '5fb3d955a985...', 'match': False}

- **cm_wkcnt->weeks_claimed**: {'legacy_checksum': '5b9d4712c411...', 'modern_checksum': '4e3b4342d241...', 'match': False}

- **cm_stat->claim_status**: {'legacy_checksum': '60fbbe4a3f13...', 'modern_checksum': '916ea1a9a595...', 'match': False}

- **cm_lupdt->updated_at**: {'legacy_checksum': '8be444881357...', 'modern_checksum': '74202d86198f...', 'match': False}

- **_summary**: {'total_columns': 13, 'matches': 0, 'mismatches': 13, 'match_rate': 0.0}


## referential_integrity — SKIP

Severity: INFO | Penalty: 0

- **reason**: No FK checks configured for claims


## sample_compare — PASS

Severity: INFO | Penalty: 0.0

- **sample_size**: 12

- **exact_matches**: 12

- **discrepancies**: 0

- **match_rate**: 100.0

- **sample_discrepancies**: []


## aggregates — SKIP

Severity: INFO | Penalty: 0

- **reason**: No aggregate checks configured for claims


## archived_leakage — PASS

Severity: INFO | Penalty: 0

- **violations**: []

- **violation_count**: 0


## unmapped_columns — PASS

Severity: INFO | Penalty: 0

- **ungoverned_columns**: []

- **count**: 0


## normalization_integrity — SKIP

Severity: INFO | Penalty: 0

- **reason**: Not a normalized dataset


## encoding — PASS

Severity: INFO | Penalty: 0

- **columns_checked**: 2

- **sample_size**: 1000

- **issue_count**: 0

- **issues**: []
