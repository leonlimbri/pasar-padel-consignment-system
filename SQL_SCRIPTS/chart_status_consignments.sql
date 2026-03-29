with cte_new as (
    select 1 as ord, status, count(*) as cnt
    from consignments
    where status = 'New'
    group by status
),
cte_posted as (
    select 2 as ord, status, count(*) as cnt
    from consignments
    where status = 'Posted'
        and consignment_date between '{start_date}' and '{end_date}'
    group by status
),
cte_sold as (
    select 
        case 
            when status = 'Sold' then 3
            when status = 'Shipped' then 4
            when status = 'Completed' then 5
            when status = 'Completed Elsewhere' then 6
        end as ord,
        status, count(*) as cnt
    from consignments
    where sold_date between '{start_date}' and '{end_date}'
        and status in ('Sold', 'Shipped', 'Completed', 'Completed Elsewhere')
    group by status
)
select * from cte_new
union all
select * from cte_posted
union all
select * from cte_sold