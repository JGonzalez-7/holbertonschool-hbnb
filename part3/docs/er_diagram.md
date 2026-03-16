# HBnB Part 3 ER Diagram

This Mermaid ER diagram reflects the SQL schema defined in `part3/sql/schema.sql`.

```mermaid
erDiagram
    USERS {
        TEXT id PK
        TEXT created_at
        TEXT updated_at
        TEXT first_name
        TEXT last_name
        TEXT email UK
        TEXT password_hash
        INTEGER is_admin
    }

    PLACES {
        TEXT id PK
        TEXT created_at
        TEXT updated_at
        TEXT name
        TEXT description
        REAL price
        REAL latitude
        REAL longitude
        TEXT owner_id FK
    }

    REVIEWS {
        TEXT id PK
        TEXT created_at
        TEXT updated_at
        INTEGER rating
        TEXT comment
        TEXT user_id FK
        TEXT place_id FK
    }

    AMENITIES {
        TEXT id PK
        TEXT created_at
        TEXT updated_at
        TEXT name UK
    }

    PLACE_AMENITY {
        TEXT place_id PK, FK
        TEXT amenity_id PK, FK
    }

    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : receives
    PLACES ||--o{ PLACE_AMENITY : includes
    AMENITIES ||--o{ PLACE_AMENITY : assigns
```

## Relationship Summary

- One user can own many places.
- One user can write many reviews.
- One place can have many reviews.
- Places and amenities are linked through the `place_amenity` join table.
- `reviews(user_id, place_id)` is unique, preventing duplicate reviews from the same user for the same place.
