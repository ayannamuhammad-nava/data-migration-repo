-- Transform script: claimants → claimants
-- Review and customize before execution

INSERT INTO claimants (
    claimant_id,
    first_name,
    last_name,
    ssn,
    date_of_birth,
    bank_account,
    bank_routing,
    registered_at,
    is_deceased,
    fil1,
    phone_number,
    email,
    created_at,
    updated_at
)
SELECT
    cl_recid,
    cl_fnam,
    cl_lnam,
    cl_ssn,
    cl_dob,
    cl_bact,
    cl_brtn,
    cl_rgdt,
    cl_dcsd,
    cl_fil1,
    cl_phon,
    cl_emal,
    NOW(),
    NOW()
FROM claimants;
