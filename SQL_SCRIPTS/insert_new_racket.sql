insert into items values (
    (select max(item_id) from items) + 1,
    '{item_type}',
    '{item_name}',
    (select brand_id from brands where brand_name = '{brand_name}'),
    {is_racket_woman},
    (select shape_id from shapes where shape_name = '{racket_shape}'),
    '{racket_additional_spec}',
    '{racket_weight}',
    (select material_id from materials where material_name = '{racket_face_material}'),
    (select material_id from materials where material_name = '{racket_core_material}')
)