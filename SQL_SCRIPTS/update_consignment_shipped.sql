update consignments
set tracking_id='{tracking_code}',
    status = 'Shipped'
where consignment_id in ('{consignment_ids}')