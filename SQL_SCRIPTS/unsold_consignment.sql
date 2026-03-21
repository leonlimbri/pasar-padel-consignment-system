update consignments
set status = 'Posted',
    tracking_id=null,
    sold_in_pasarpadel = null,
    buyer_id = null,
    price_sold = null,
    sales_id = null
where consignment_id = '{consignment_id}'