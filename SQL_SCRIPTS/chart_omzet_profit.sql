with the_sold as (
    select
        sold_date as the_date,    
        SUM(CASE WHEN status IN ('Completed', 'Shipped', 'Sold') THEN price_sold ELSE 0 END) AS total_omzet,
        SUM(CASE WHEN status IN ('Completed') THEN price_sold - price_modal ELSE 0 END) AS total_profit,
        SUM(CASE WHEN status IN ('Completed', 'Shipped', 'Sold') THEN 1 ELSE 0 END) AS total_terjual
    from consignments
    where sold_date between '{start_date}' and '{end_date}'
    group by sold_date
),
the_consigned as (
    select
        consignment_date as the_date,
        count(*) as total_consigned
    from consignments
    where consignment_date between '{start_date}' and '{end_date}'
        and status = 'Posted'
    group by consignment_date
),
final as (
    select * from the_sold
    full outer join the_consigned using (the_date)
)
select the_date, coalesce(total_omzet, 0) as total_omzet, coalesce(total_profit, 0) as total_profit, coalesce(total_terjual, 0) as total_terjual, coalesce(total_consigned, 0) as total_consigned
from final
order by the_date