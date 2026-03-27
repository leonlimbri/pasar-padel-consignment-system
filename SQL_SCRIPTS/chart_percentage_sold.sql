WITH cte AS (
    SELECT *
    FROM consignments c
    WHERE c.consignment_date BETWEEN '{start_date}' AND '{end_date}'
        AND status in ('Completed', 'Completed Elsewhere')
)
SELECT s.label, s.status, COUNT(c.status) AS pcnt
FROM (
    SELECT "Terjual di Pasar Padel" AS label, 'Completed'   AS status UNION ALL
    SELECT "Terjual di Tempat Lain", 'Completed Elsewhere'  AS status
) AS s
LEFT JOIN cte c ON c.status = s.status
GROUP BY s.status