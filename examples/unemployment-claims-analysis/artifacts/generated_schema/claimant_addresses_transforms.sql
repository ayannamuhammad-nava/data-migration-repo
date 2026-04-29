-- Transform script: claimants → claimant_addresses
-- Review and customize before execution

INSERT INTO claimant_addresses (
    address_line1,
    city,
    state,
    zip_code,
    status,
    created_at,
    updated_at
)
SELECT
    cl_adr1,
    cl_city,
    cl_st,
    cl_zip,
    cl_stat,
    NOW(),
    NOW()
FROM claimants;
