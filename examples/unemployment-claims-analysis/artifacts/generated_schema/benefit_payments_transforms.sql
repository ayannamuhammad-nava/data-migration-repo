-- Transform script: benefit_payments → benefit_payments
-- Review and customize before execution

INSERT INTO benefit_payments (
    benefit_payment_id,
    claim_id,
    paydt,
    payment_amount,
    methd,
    wkedt,
    chkno,
    status,
    created_at,
    updated_at
)
SELECT
    bp_recid,
    bp_clmid,
    bp_paydt,
    bp_payam,
    bp_methd,
    bp_wkedt,
    bp_chkno,
    bp_stat,
    NOW(),
    NOW()
FROM benefit_payments;
