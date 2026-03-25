select
    item_name,
    count(*) as total_consigned,
    sum(case when status in ('Completed', 'Shipped', 'Sold') then 1 else 0 end) as total_sold,
    avg(case when status in ('Completed', 'Shipped', 'Sold') then price_sold else 0 end) as average_omzet,
    avg(case when status in ('Completed', 'Shipped', 'Sold') then price_sold - price_modal else 0 end) as average_profit
from consignments
where consignment_date between '{start_date}' and '{end_date}'
    and item_name <> '0'
group by item_name
having count(*) > 0