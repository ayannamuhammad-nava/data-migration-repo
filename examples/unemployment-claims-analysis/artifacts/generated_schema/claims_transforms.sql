-- Transform script: claims → claims
-- Review and customize before execution

INSERT INTO claims (
    claim_id,
    claimant_id,
    employer_id,
    seprs,
    filing_date,
    benefit_year_end,
    weekly_amount,
    mxamt,
    totpd,
    wkcnt,
    lupdt,
    benefit_year_start,
    status,
    created_at,
    updated_at
)
SELECT
    cm_recid,
    cm_clmnt,
    cm_emplr,
    cm_seprs,
    cm_fildt,
    cm_byend,
    cm_wkamt,
    cm_mxamt,
    cm_totpd,
    cm_wkcnt,
    cm_lupdt,
    cm_bystr,
    cm_stat,
    NOW(),
    NOW()
FROM claims;
