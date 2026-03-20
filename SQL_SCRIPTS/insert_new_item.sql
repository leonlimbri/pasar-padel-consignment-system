insert into items values (
    (select max(item_id) from items) + 1,
    '{item_type}',
    '{item_name}',
    (select brand_id from brands where brand_name = '{brand_name}'),
    null,
    null,
    null,
    null,
    null,
    null
)