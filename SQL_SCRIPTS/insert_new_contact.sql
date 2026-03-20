insert into contacts values (
    (select max(contact_id) from contacts) + 1,
    '{contact_wa}',
    '{contact_name}',
    '{contact_location}'
)