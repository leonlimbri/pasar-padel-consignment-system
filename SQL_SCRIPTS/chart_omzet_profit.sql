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
        SUM(CASE WHEN status IN ('New', 'Posted') THEN 1 ELSE 0 END) AS total_consigned
    from consignments
    where consignment_date between '{start_date}' and '{end_date}'
    group by consignment_date
)
select * from the_sold
join the_consigned using (the_date)