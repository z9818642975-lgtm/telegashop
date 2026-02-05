BEGIN;

-- USERS
INSERT INTO users (tg_id, role)
VALUES
    (7444294101, 'ADMIN'),
    (8413852743, 'OPERATOR')
ON CONFLICT (tg_id) DO UPDATE SET role = EXCLUDED.role;

-- PRODUCTS (6)
INSERT INTO products (title, description, base_price, min_qty, is_active)
VALUES
    ('🎮 Мяу', '1 шт = 4000, от 2 шт = 3500₽/шт', 4000, 1, TRUE),
    ('📚 Кок', '1 шт = 12000₽, от 2 шт = 11000₽/шт', 12000, 1, TRUE),
    ('🍫 Экс', 'Продаётся от 2 шт', 1500, 2, TRUE),
    ('⚽️ Гар', NULL, 1800, 1, TRUE),
    ('🎨 Бош', NULL, 1800, 1, TRUE),
    ('🤖 Лир', NULL, 4000, 1, TRUE)
ON CONFLICT (title) DO NOTHING;

-- WAREHOUSE
INSERT INTO warehouses (title, address, owner_id, is_active)
SELECT
    'Основной склад',
    'г. Москва, тестовый адрес',
    u.id,
    TRUE
FROM users u
WHERE u.role = 'ADMIN'
LIMIT 1
ON CONFLICT DO NOTHING;

-- BANK ACCOUNTS
INSERT INTO bank_accounts (
    bank_name, card_number, card_masked, sbp_phone, is_active, load, weight
)
VALUES
    ('Сбербанк', '2202208208297771', '2202 **** **** 7771', NULL, TRUE, 0, 100),
    ('Сбербанк', '4276550062549103', '4276 **** **** 9103', NULL, TRUE, 0, 100),
    ('Сбербанк', NULL, NULL, '9817815379', TRUE, 0, 100),
    ('Сбербанк', NULL, NULL, '9818642975', TRUE, 0, 100),
    ('Т-Банк', NULL, NULL, '9818642975', TRUE, 0, 100),
    ('Т-Банк', '2200700988565783', '2200 **** **** 5783', NULL, TRUE, 0, 100),
    ('Альфа-Банк', '2200152314652077', '2200 **** **** 2077', NULL, TRUE, 0, 100),
    ('Альфа-Банк', NULL, NULL, '9818642975', TRUE, 0, 100);

COMMIT;
