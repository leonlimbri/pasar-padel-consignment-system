with cte as (
    select
        i.item_id,
        i.item_type,
        i.item_name,
        i.is_racket_woman,
        i.racket_additional_spec,
        i.racket_weight,
        b.brand_name,
        s.shape_name,
        f.material_name as face_material,    
        c.material_name as core_material
    from items i
    left join brands b on i.item_brand_id = b.brand_id
    left join shapes s on i.racket_shape_id = s.shape_id
    left join materials f on i.racket_face_id = f.material_id
    left join materials c on i.racket_core_id = c.material_id
)

select *
from cte
where item_type='{item_type}'
    and brand_name='{brand_name}'
    and item_name='{item_name}'