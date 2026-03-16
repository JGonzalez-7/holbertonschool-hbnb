# HBnB Part 3

Starter structure for the Part 3 backend, focused on authentication and database integration.

## Structure
- `app/` application package and Flask extensions
- `app/persistence/` SQLAlchemy repository implementation
- `app/services/` facade layer using the repository for user persistence
- `docs/` Mermaid documentation for the database schema
- `instance/` local runtime files such as SQLite databases
- `tests/` automated tests
- `venv/` local virtual environment folder
- `.env` local development variables
- `config.py` environment-specific configuration
- `run.py` development entrypoint

## Quickstart
```bash
cd part3/hbnb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run --host=0.0.0.0 --port=8000
```

## SQLAlchemy Repository
Part 3 now includes a repository layer in `app/persistence/repository.py` and a facade in `app/services/facade.py`.

Integration notes:
- `create_app()` registers `HBnBFacade` on `app.extensions["facade"]`.
- `app/models/base.py` maps the shared `id`, `created_at`, and `updated_at` fields for ORM-backed entities.
- `app/persistence/user_repository.py` provides a dedicated `UserRepository` on top of the generic `SQLAlchemyRepository`.
- `Place`, `Review`, and `Amenity` are also mapped as SQLAlchemy models using the shared base model.
- SQLAlchemy relationships now connect users, places, reviews, and amenities through foreign keys and the `place_amenity` association table.
- The API namespaces retrieve the facade from `app.extensions["facade"]` and delegate persistence operations through the repository-backed service layer.

## SQL Scripts
Raw SQL scripts for the Part 3 database live in `part3/sql/`:

- `schema.sql`: creates the full SQLite schema, including foreign keys and the `place_amenity` join table
- `seed_data.sql`: inserts one administrator user and default amenities
- `verify_crud.sql`: runs sample CRUD operations inside a transaction and rolls them back

Example usage:

```bash
sqlite3 part3/instance/hbnb.db < part3/sql/schema.sql
sqlite3 part3/instance/hbnb.db < part3/sql/seed_data.sql
sqlite3 part3/instance/hbnb.db < part3/sql/verify_crud.sql
```

Seeded administrator account:
- email: `admin@hbnb.io`
- password: `admin1234`

## ER Diagram
The Mermaid ER diagram for the current database schema is documented in `part3/docs/er_diagram.md`.
