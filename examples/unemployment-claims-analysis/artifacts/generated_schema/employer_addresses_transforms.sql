-- Transform script: employers → employer_addresses
-- Review and customize before execution

INSERT INTO employer_addresses (
    address_line1,
    city,
    state,
    zip_code,
    status,
    created_at,
    updated_at
)
SELECT
    er_adr1,
    er_city,
    er_st,
    er_zip,
    er_stat,
    NOW(),
    NOW()
FROM employers;
