WITH cte AS (
    SELECT *
    FROM consignments c
    WHERE c.consignment_date BETWEEN '{start_date}' AND '{end_date}'
)
SELECT s.status, COUNT(c.status) AS cnt
FROM (
    SELECT 1 AS ord, 'New'           AS status UNION ALL
    SELECT 2, 'Posted'               AS status UNION ALL
    SELECT 3, 'Sold'                 AS status UNION ALL
    SELECT 4, 'Shipped'              AS status UNION ALL
    SELECT 5, 'Completed'            AS status UNION ALL
    SELECT 6, 'Completed Elsewhere'  AS status
) AS s
LEFT JOIN cte c ON c.status = s.status
GROUP BY s.status
ORDER BY s.ord