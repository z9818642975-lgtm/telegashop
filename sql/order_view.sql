DROP VIEW IF EXISTS order_items_view;

CREATE VIEW order_items_view AS
SELECT
    o.id                 AS order_id,
    o.client_id          AS client_tg_id,
    o.status             AS order_status,
    o.created_at         AS order_created_at,

    oi.id                AS order_item_id,
    oi.product_id        AS product_id,
    p.title              AS product_title,
    oi.qty               AS qty,
    oi.price             AS price,
    (oi.qty * oi.price)  AS line_total,
    oi.status            AS item_status

FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id;

