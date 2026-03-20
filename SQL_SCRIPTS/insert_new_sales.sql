insert into sales values (
    (select max(sale_id) from sales) + 1,
    '{sales_name}'
)