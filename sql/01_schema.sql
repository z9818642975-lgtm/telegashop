BEGIN;

-- =========================
-- EXTENSIONS
-- =========================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- ENUMS
-- =========================
DO $$ BEGIN
    CREATE TYPE userrole AS ENUM ('ADMIN', 'OPERATOR', 'CLIENT');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE orderstatus AS ENUM ('CART','WAITING_PAYMENT','WAITING_OPERATOR','ACCEPTED','PAID','SENT','DONE','CANCELLED');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE orderitemstatus AS ENUM ('NEW','ACCEPTED','PAID','DONE');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE paymentmethod AS ENUM ('CARD','SBP','CASH');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

DO $$ BEGIN
    CREATE TYPE paymentstatus AS ENUM ('NEW','APPROVED','REJECTED');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- =========================
-- USERS
-- =========================
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    tg_id BIGINT NOT NULL UNIQUE,
    role userrole NOT NULL DEFAULT 'CLIENT',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- =========================
-- PRODUCTS
-- =========================
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    base_price INTEGER NOT NULL CHECK (base_price >= 0),
    min_qty INTEGER NOT NULL DEFAULT 1 CHECK (min_qty > 0),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_products_title ON products(title);

-- =========================
-- WAREHOUSES
-- =========================
CREATE TABLE IF NOT EXISTS warehouses (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    owner_id BIGINT NOT NULL REFERENCES users(id),
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- =========================
-- ORDERS
-- =========================
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    client_id BIGINT NOT NULL REFERENCES users(id),
    operator_id BIGINT REFERENCES users(id),
    status orderstatus NOT NULL DEFAULT 'CART',
    total_price INTEGER NOT NULL DEFAULT 0,

    pickup_comment TEXT,
    pickup_photo_id TEXT,

    payment_proof_file_id TEXT,
    payment_proof_type TEXT,
    payment_submitted_at TIMESTAMP,
    payment_checked_at TIMESTAMP,
    paid_at TIMESTAMP,

    sla_deadline TIMESTAMP,
    completed_at TIMESTAMP,

    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

-- =========================
-- ORDER ITEMS
-- =========================
CREATE TABLE IF NOT EXISTS order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES products(id),
    qty INTEGER NOT NULL CHECK (qty > 0),
    price INTEGER NOT NULL CHECK (price >= 0),
    status orderitemstatus NOT NULL DEFAULT 'NEW',
    completed_at TIMESTAMP
);

-- =========================
-- OPERATOR SHIFTS (tg_id!)
-- =========================
CREATE TABLE IF NOT EXISTS operator_shifts (
    id BIGSERIAL PRIMARY KEY,
    operator_id BIGINT NOT NULL REFERENCES users(tg_id),
    pickup_address TEXT NOT NULL,
    started_at TIMESTAMP NOT NULL DEFAULT now(),
    ended_at TIMESTAMP,
    last_activity_at TIMESTAMP,
    warned_15 BOOLEAN NOT NULL DEFAULT FALSE,
    warned_17 BOOLEAN NOT NULL DEFAULT FALSE,
    warned_20 BOOLEAN NOT NULL DEFAULT FALSE,
    auto_closed BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS ix_operator_shifts_active
    ON operator_shifts (ended_at)
    WHERE ended_at IS NULL;

-- =========================
-- BANK ACCOUNTS
-- =========================
CREATE TABLE IF NOT EXISTS bank_accounts (
    id BIGSERIAL PRIMARY KEY,
    bank_name VARCHAR(64) NOT NULL,
    card_number VARCHAR(32),
    card_masked VARCHAR(32),
    sbp_phone VARCHAR(16),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    disabled_until TIMESTAMP,
    load INTEGER NOT NULL DEFAULT 0,
    weight INTEGER NOT NULL DEFAULT 100
);

-- =========================
-- PAYMENTS
-- =========================
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

COMMIT;
