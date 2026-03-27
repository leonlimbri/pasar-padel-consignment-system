update consignments
set link_ig='{link_ig}',
    status = 'Posted',
    consignment_date = '{consignment_date}'
where consignment_id in ('{consignment_ids}')