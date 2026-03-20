insert into materials values (
    (select max(material_id) from materials) + 1,
    '{material_type}',
    '{material_name}'
)