update consignments
set link_ig='{link_ig}',
    status = 'Posted'
where consignment_id in ('{consignment_ids}')