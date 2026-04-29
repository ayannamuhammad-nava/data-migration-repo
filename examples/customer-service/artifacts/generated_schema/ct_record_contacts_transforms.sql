-- Transform script: contacts → ct_record_contacts
-- Review and customize before execution

INSERT INTO ct_record_contacts (
    primary_phone,
    mobile_phone,
    work_phone,
    email,
    emergency_contact_phone,
    created_at,
    updated_at
)
SELECT
    ct_ptel,
    ct_mtel,
    ct_wtel,
    ct_emal,
    ct_etel,
    NOW(),
    NOW()
FROM contacts;
