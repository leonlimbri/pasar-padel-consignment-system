with the_sold as (
    select
        item_name,
        sum(case when status in ('Completed', 'Shipped', 'Sold') then 1 else 0 end) as total_sold,
        avg(case when status in ('Completed', 'Shipped', 'Sold') then price_sold else 0 end) as average_omzet,
        avg(case when status in ('Completed', 'Shipped', 'Sold') then price_sold - price_modal else 0 end) as average_profit
    from consignments
    where sold_date between '{start_date}' and '{end_date}'
        and item_name <> '0'
    group by item_name
),
the_consigned as (
    select
        item_name,
        sum(case when status in ('New', 'Posted') then 1 else 0 end) as total_consigned
    from consignments
    where consignment_date between '{start_date}' and '{end_date}'
        and item_name <> '0'
    group by item_name
)
select * from the_sold
join the_consigned using (item_name)