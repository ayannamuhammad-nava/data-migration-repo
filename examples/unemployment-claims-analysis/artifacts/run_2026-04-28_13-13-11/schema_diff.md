# Schema Diff Report: claimants

## Columns Missing in Modern System

- **cl_adr1** (character varying)
- **cl_brtn** (character)
- **cl_city** (character)
- **cl_dcsd** (character)
- **cl_dob** (character)
- **cl_emal** (character varying)
- **cl_fil1** (character)
- **cl_fnam** (character)
- **cl_lnam** (character)
- **cl_phon** (character)
- **cl_recid** (integer)
- **cl_rgdt** (character)
- **cl_ssn** (character)
- **cl_st** (character)
- **cl_stat** (character)
- **cl_zip** (character)

## New Columns in Modern System

- **address_line1** (character varying)
- **city** (character varying)
- **claimant_id** (integer)
- **claimant_status** (character varying)
- **date_of_birth** (date)
- **email** (character varying)
- **first_name** (character varying)
- **is_deceased** (boolean)
- **last_name** (character varying)
- **legacy_system_ref** (character varying)
- **phone_number** (bigint)
- **registered_at** (timestamp without time zone)
- **ssn_hash** (character varying)
- **state** (character varying)
- **zip_code** (character varying)

## Type Mismatches

| Column | Legacy Type | Modern Type |
|--------|-------------|-------------|
| cl_bact | character | character varying |

## Summary

- Common columns: 1
- Missing in modern: 16
- New in modern: 15
- Type mismatches: 1
