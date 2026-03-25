SELECT
    consignment_date,
    SUM(CASE WHEN status IN ('Completed', 'Shipped', 'Sold') THEN price_sold ELSE 0 END) AS total_omzet,
    SUM(CASE WHEN status IN ('Completed') THEN price_sold - price_modal ELSE 0 END) AS total_profit,
    SUM(CASE WHEN status IN ('Completed', 'Shipped', 'Sold') THEN 1 ELSE 0 END) AS total_terjual,
    SUM(CASE WHEN status IN ('New', 'Posted') THEN 1 ELSE 0 END) AS total_consigned
FROM consignments
WHERE consignment_date BETWEEN '{start_date}' AND '{end_date}'
GROUP BY consignment_date