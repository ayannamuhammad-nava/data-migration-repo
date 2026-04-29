-- Transform script: employers → employers
-- Review and customize before execution

INSERT INTO employers (
    employer_id,
    name,
    ein,
    indicator,
    phone_number,
    created_at,
    updated_at
)
SELECT
    er_recid,
    er_name,
    er_ein,
    er_ind,
    er_phon,
    NOW(),
    NOW()
FROM employers;
