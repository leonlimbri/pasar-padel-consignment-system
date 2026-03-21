update consignments
set sold_in_pasarpadel = {sold_in_pasarpadel},
    buyer_id = (select contact_id from contacts where contact_wa='{buyer_wa}'),
    price_sold = {price_sold},
    sales_id = (select sales_id from sales where sales_name='{sales_name}'),
    status = 'Sold'
where consignment_id='{consignment_id}'