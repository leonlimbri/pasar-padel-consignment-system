insert into brands values (
    (select max(brand_id) from brands) + 1,
    '{brand_name}'
)