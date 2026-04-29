# Schema Diff Report: benefit_payments

## Columns Missing in Modern System

- **bp_chkno** (character)
- **bp_clmid** (integer)
- **bp_methd** (character)
- **bp_payam** (numeric)
- **bp_paydt** (character)
- **bp_recid** (integer)
- **bp_stat** (character)
- **bp_wkedt** (character)

## New Columns in Modern System

- **check_number** (character varying)
- **claim_id** (integer)
- **payment_amount** (numeric)
- **payment_date** (date)
- **payment_id** (integer)
- **payment_method** (character varying)
- **payment_status** (character varying)
- **week_ending_date** (date)

## Summary

- Common columns: 0
- Missing in modern: 8
- New in modern: 8
- Type mismatches: 0
