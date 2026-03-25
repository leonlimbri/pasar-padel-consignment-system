select
    s.sales_name,
    count(*) as total_consigned,
    sum(case when c.status in ('Completed', 'Shipped', 'Sold') then 1 else 0 end) as total_sold,
    sum(case when c.status in ('Completed', 'Shipped', 'Sold') then price_sold else 0 end) as total_omset
from sales s
left join consignments c on s.sales_id = c.sales_id
where c.consignment_date between '{start_date}' and '{end_date}'
group by s.sales_name