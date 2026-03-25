select
    s.sales_name,
    sum(case when c.status in ('Completed', 'Shipped', 'Sold') then 1 else 0 end) as total_sold,
    sum(case when c.status in ('Completed', 'Shipped', 'Sold') then price_sold else 0 end) as total_omset,
    sum(case when c.status in ('Completed') then price_sold - price_modal else 0 end) as total_profit
from sales s
left join consignments c on s.sales_id = c.sales_id
where c.consignment_date between '{start_date}' and '{end_date}'
group by s.sales_name