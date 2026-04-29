-- Transform script: contacts → ct_record_addresses
-- Review and customize before execution

INSERT INTO ct_record_addresses (
    address_line1,
    address_line2,
    city,
    state,
    zip_code,
    mailing_address_line1,
    mailing_address_line2,
    mailing_city,
    mailing_state,
    mailing_zip_code,
    drivers_license_state,
    marital_status,
    marital_status,
    created_at,
    updated_at
)
SELECT
    ct_adr1,
    ct_adr2,
    ct_city,
    ct_st,
    ct_zip,
    ct_madr1,
    ct_madr2,
    ct_mcity,
    ct_mst,
    ct_mzip,
    ct_dlst,
    ct_mstat,
    ct_stat,
    NOW(),
    NOW()
FROM contacts;
