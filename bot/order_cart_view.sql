CREATE OR REPLACE VIEW order_cart_view AS
SELECT
    o.id AS order_id,
    o.client_id,
    COUNT(oi.id) AS total_items,
    COUNT(*) FILTER (WHERE oi.status = 'ACCEPTED') AS accepted_items,
    COUNT(*) FILTER (WHERE oi.status = 'PAID')     AS paid_items,
    COUNT(*) FILTER (WHERE oi.status = 'DONE')     AS done_items,
    BOOL_AND(oi.status = 'DONE') AS is_completed
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id, o.client_id;
