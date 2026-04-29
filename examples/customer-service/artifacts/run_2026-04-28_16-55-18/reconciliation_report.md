# Post-Migration Reconciliation Report: contacts


## row_count — PASS

Severity: INFO | Penalty: 0.0

- **legacy_count**: 0

- **modern_count**: 0

- **match**: True

- **difference**: 0


## checksums — PASS

Severity: INFO | Penalty: 0

- **ct_recid->contact_id**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_fnam->first_name**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_mnam->middle_name**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_lnam->last_name**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_sufx->name_suffix**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_gndr->gender**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_ethn->ethnicity**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_ptel->primary_phone**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_mtel->mobile_phone**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_wtel->work_phone**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_emal->email**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_adr1->address_line1**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_adr2->address_line2**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_city->city**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_st->state**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_adtyp->address_type**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_madr1->mailing_address_line1**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_madr2->mailing_address_line2**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_mcity->mailing_city**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_mst->mailing_state**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_emrg->emergency_contact_name**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_etel->emergency_contact_phone**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_erel->emergency_contact_relation**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_dln->drivers_license_number**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_dlst->drivers_license_state**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_mstat->marital_status**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_dpnds->dependents_count**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_lang->language_preference**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_vetf->is_veteran**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_disf->is_disabled**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_stat->marital_status**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_crtdt->created_at**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_upddt->updated_at**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **ct_srccd->source_code**: {'legacy_checksum': 'N/A', 'modern_checksum': 'N/A', 'match': True}

- **_summary**: {'total_columns': 34, 'matches': 34, 'mismatches': 0, 'match_rate': 100.0}


## referential_integrity — SKIP

Severity: INFO | Penalty: 0

- **reason**: No FK checks configured for contacts


## sample_compare — SKIP

Severity: INFO | Penalty: 0

- **note**: No records in legacy


## aggregates — SKIP

Severity: INFO | Penalty: 0

- **reason**: No aggregate checks configured for contacts


## archived_leakage — PASS

Severity: INFO | Penalty: 0

- **violations**: []

- **violation_count**: 0


## unmapped_columns — WARN

Severity: MEDIUM | Penalty: 5

- **ungoverned_columns**: ['contact_status']

- **count**: 1


## normalization_integrity — PASS

Severity: INFO | Penalty: 0

- **issue_count**: 0

- **issues**: []

- **modern_tables**: ['contacts']

- **legacy_row_count**: 0

- **primary_table**: contacts


## encoding — PASS

Severity: INFO | Penalty: 0

- **columns_checked**: 20

- **sample_size**: 1000

- **issue_count**: 0

- **issues**: []
