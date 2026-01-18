CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- ENUMS
-- =========================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN
        CREATE TYPE userrole AS ENUM ('ADMIN', 'OPERATOR', 'CLIENT');
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'orderitemstatus') THEN
        CREATE TYPE orderitemstatus AS ENUM ('NEW', 'ACCEPTED', 'PAID', 'DONE');
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'orderstatus') THEN
        CREATE TYPE orderstatus AS ENUM ('NEW', 'PAID', 'DONE', 'CANCELLED');
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'paymentmethod') THEN
        CREATE TYPE paymentmethod AS ENUM ('CARD', 'SBP', 'CASH');
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'paymentstatus') THEN
        CREATE TYPE paymentstatus AS ENUM ('NEW', 'APPROVED', 'REJECTED');
    END IF;
END$$;

-- =========================
-- USERS
-- =========================
CREATE TABLE users (
    id         BIGSERIAL PRIMARY KEY,
    tg_id      BIGINT NOT NULL UNIQUE,
    role       userrole NOT NULL DEFAULT 'CLIENT',
    is_active  BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- =========================
-- PRODUCTS
-- =========================
CREATE TABLE products (
    id          BIGSERIAL PRIMARY KEY,
    title       VARCHAR(255) NOT NULL,
    description TEXT,
    base_price  INTEGER NOT NULL CHECK (base_price >= 0),
    min_qty     INTEGER NOT NULL DEFAULT 1 CHECK (min_qty > 0),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE UNIQUE INDEX uq_products_title ON products(title);

-- =========================
-- WAREHOUSES
-- =========================
CREATE TABLE warehouses (
    id        BIGSERIAL PRIMARY KEY,
    title     VARCHAR(255) NOT NULL,
    address   TEXT NOT NULL,
    owner_id  BIGINT NOT NULL REFERENCES users(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- =========================
-- ORDERS
-- =========================
CREATE TABLE orders (
    id          BIGSERIAL PRIMARY KEY,
    client_id  BIGINT NOT NULL REFERENCES users(tg_id),
    status      orderstatus NOT NULL DEFAULT 'NEW',
    created_at  TIMESTAMP NOT NULL DEFAULT now()
);

-- =========================
-- ORDER ITEMS
-- =========================
CREATE TABLE order_items (
    id           BIGSERIAL PRIMARY KEY,
    order_id     BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id   BIGINT NOT NULL REFERENCES products(id),
    qty          INTEGER NOT NULL CHECK (qty > 0),
    price        INTEGER NOT NULL CHECK (price >= 0),
    status       orderitemstatus NOT NULL DEFAULT 'NEW',
    completed_at TIMESTAMP
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_status ON order_items(status);

-- =========================
-- OPERATOR SHIFTS
-- =========================
CREATE TABLE operator_shifts (
    id             BIGSERIAL PRIMARY KEY,
    operator_id    BIGINT NOT NULL REFERENCES users(tg_id),
    pickup_address TEXT NOT NULL,
    started_at     TIMESTAMP NOT NULL DEFAULT now(),
    ended_at       TIMESTAMP,
    auto_closed    BOOLEAN NOT NULL DEFAULT FALSE
);

-- =========================
-- BANK ACCOUNTS
-- =========================
CREATE TABLE bank_accounts (
    id          BIGSERIAL PRIMARY KEY,
    bank_name   VARCHAR(64) NOT NULL,
    card_number VARCHAR(32),
    card_masked VARCHAR(32),
    sbp_phone   VARCHAR(16),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    load        INTEGER NOT NULL DEFAULT 0,
    weight      INTEGER NOT NULL DEFAULT 100
);

CREATE TABLE IF NOT EXISTS payments (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    bank_account_id BIGINT NOT NULL REFERENCES bank_accounts(id),
    method paymentmethod NOT NULL,
    status paymentstatus NOT NULL,
    amount INTEGER NOT NULL,
    requisites VARCHAR(255) NOT NULL,
    check_file_id VARCHAR(255),
    reject_reason VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    approved_at TIMESTAMP,
    rejected_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id);

-- =========================
-- VIEW
-- =========================
DROP VIEW IF EXISTS order_view;

CREATE VIEW order_view AS
SELECT
    o.id AS order_id,
    COUNT(oi.id) AS total_items,
    COUNT(*) FILTER (WHERE oi.status = 'PAID') AS paid_items,
    COUNT(*) FILTER (WHERE oi.status = 'DONE') AS done_items,
    BOOL_AND(oi.status = 'DONE') AS is_completed
FROM orders o
LEFT JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id;

