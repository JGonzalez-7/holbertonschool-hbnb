PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

INSERT INTO users (
    id,
    created_at,
    updated_at,
    first_name,
    last_name,
    email,
    password_hash,
    is_admin
) VALUES (
    '30000000-0000-0000-0000-000000000001',
    '2026-03-13T00:10:00',
    '2026-03-13T00:10:00',
    'Test',
    'Owner',
    'owner@example.com',
    '$2y$12$J0FRCkjvy39EtH6/LyhzKu.Ooivofpo98aHvRtwaAzRJFYtSVcRT.',
    0
);

INSERT INTO users (
    id,
    created_at,
    updated_at,
    first_name,
    last_name,
    email,
    password_hash,
    is_admin
) VALUES (
    '30000000-0000-0000-0000-000000000002',
    '2026-03-13T00:11:00',
    '2026-03-13T00:11:00',
    'Test',
    'Reviewer',
    'reviewer@example.com',
    '$2y$12$J0FRCkjvy39EtH6/LyhzKu.Ooivofpo98aHvRtwaAzRJFYtSVcRT.',
    0
);

INSERT INTO places (
    id,
    created_at,
    updated_at,
    name,
    description,
    price,
    latitude,
    longitude,
    owner_id
) VALUES (
    '40000000-0000-0000-0000-000000000001',
    '2026-03-13T00:20:00',
    '2026-03-13T00:20:00',
    'Test Loft',
    'Schema verification place',
    99.50,
    18.2208,
    -66.5901,
    '30000000-0000-0000-0000-000000000001'
);

INSERT INTO place_amenity (place_id, amenity_id) VALUES
    ('40000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000001'),
    ('40000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000002');

INSERT INTO reviews (
    id,
    created_at,
    updated_at,
    rating,
    comment,
    user_id,
    place_id
) VALUES (
    '50000000-0000-0000-0000-000000000001',
    '2026-03-13T00:30:00',
    '2026-03-13T00:30:00',
    5,
    'Excellent test stay',
    '30000000-0000-0000-0000-000000000002',
    '40000000-0000-0000-0000-000000000001'
);

SELECT 'users_count', COUNT(*) FROM users;
SELECT 'amenities_count', COUNT(*) FROM amenities;
SELECT 'places_count', COUNT(*) FROM places;
SELECT 'reviews_count', COUNT(*) FROM reviews;

SELECT
    p.name,
    u.email AS owner_email,
    COUNT(r.id) AS review_count
FROM places AS p
JOIN users AS u ON u.id = p.owner_id
LEFT JOIN reviews AS r ON r.place_id = p.id
WHERE p.id = '40000000-0000-0000-0000-000000000001'
GROUP BY p.id, p.name, u.email;

UPDATE places
SET
    price = 120.00,
    updated_at = '2026-03-13T00:40:00'
WHERE id = '40000000-0000-0000-0000-000000000001';

SELECT 'updated_price', price
FROM places
WHERE id = '40000000-0000-0000-0000-000000000001';

DELETE FROM reviews
WHERE id = '50000000-0000-0000-0000-000000000001';

SELECT 'reviews_after_delete', COUNT(*)
FROM reviews
WHERE place_id = '40000000-0000-0000-0000-000000000001';

ROLLBACK;
