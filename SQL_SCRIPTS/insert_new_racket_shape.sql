insert into shapes values (
    (select max(shape_id) from shapes) + 1,
    '{shape_name}'
)