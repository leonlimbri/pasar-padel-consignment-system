update consignments
set status = 'Completed'
where consignment_id in ('{consignment_ids}')