PRAGMA foreign_keys = ON;

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
    '11111111-1111-1111-1111-111111111111',
    '2026-03-13T00:00:00',
    '2026-03-13T00:00:00',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2y$12$J0FRCkjvy39EtH6/LyhzKu.Ooivofpo98aHvRtwaAzRJFYtSVcRT.',
    1
);

INSERT INTO amenities (id, created_at, updated_at, name) VALUES
    ('20000000-0000-0000-0000-000000000001', '2026-03-13T00:00:00', '2026-03-13T00:00:00', 'WiFi'),
    ('20000000-0000-0000-0000-000000000002', '2026-03-13T00:00:00', '2026-03-13T00:00:00', 'Pool'),
    ('20000000-0000-0000-0000-000000000003', '2026-03-13T00:00:00', '2026-03-13T00:00:00', 'Air Conditioning');
