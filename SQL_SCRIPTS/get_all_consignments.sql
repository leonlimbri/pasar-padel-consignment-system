with cte as (
    select
        cons.consignment_id,
        cons.item_type,
        cons.item_name,
        cons.item_weight,
        cons.item_condition,
        cons.item_rating,
        cons.extra_description,
        cons.extra_note,
        cons.price_modal,
        cons.price_posted,
        cons.link_ig,
        cons.consignment_date,
        cons.sold_date,
        cons.price_sold,
        cons.tracking_id,
        cons.sold_in_pasarpadel,
        cons.status,
        cons.consignment_status_deleted,
        sell.contact_wa as seller_wa,
        sell.contact_name as seller_name,
        sell.contact_location as seller_location,
        buyer.contact_wa as buyer_wa,
        buyer.contact_name as buyer_name,
        buyer.contact_location as buyer_location,
        sales.sales_name as sales_name,
        case when cons.item_condition = 'Used' then concat(cons.item_condition, ' (', printf('%-5s', cons.item_rating), '/10.0)') else 'New' end as item_condition_rating
    from consignments cons
    left join contacts sell on cons.seller_id = sell.contact_id
    left join contacts buyer on cons.buyer_id = buyer.contact_id
    left join sales sales on cons.sales_id = sales.sales_id
)
select * 
from cte
where item_type in {sel_types}
    and status in {sel_status}
    and consignment_status_deleted = FALSE