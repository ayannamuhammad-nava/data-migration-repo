# Schema Diff Report: claims

## Columns Missing in Modern System

- **cm_byend** (character)
- **cm_bystr** (character)
- **cm_clmnt** (integer)
- **cm_emplr** (integer)
- **cm_fildt** (character)
- **cm_lupdt** (character)
- **cm_mxamt** (numeric)
- **cm_recid** (integer)
- **cm_seprs** (character varying)
- **cm_stat** (character)
- **cm_totpd** (numeric)
- **cm_wkamt** (numeric)
- **cm_wkcnt** (integer)

## New Columns in Modern System

- **benefit_year_end** (date)
- **benefit_year_start** (date)
- **claim_id** (integer)
- **claim_status** (character varying)
- **claimant_id** (integer)
- **employer_id** (integer)
- **filing_date** (date)
- **max_benefit_amount** (numeric)
- **separation_reason** (character varying)
- **total_paid** (numeric)
- **updated_at** (timestamp without time zone)
- **weekly_benefit_amount** (numeric)
- **weeks_claimed** (integer)

## Summary

- Common columns: 0
- Missing in modern: 13
- New in modern: 13
- Type mismatches: 0
