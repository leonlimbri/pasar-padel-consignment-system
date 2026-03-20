update items
set
    item_brand_id=(select brand_id from brands where brand_name = '{brand_name}'),
    is_racket_woman={is_racket_woman},
    racket_shape_id=(select shape_id from shapes where shape_name = '{racket_shape}'),
    racket_additional_spec='{racket_additional_spec}',
    racket_weight='{racket_weight}',
    racket_face_id=(select material_id from materials where material_name = '{racket_face_material}'),
    racket_core_id=(select material_id from materials where material_name = '{racket_core_material}')
where item_name='{item_name}'
    and item_type='Racket'