# HBnB – Part 2

This part brings the HBnB architecture from Part 1 to life using Flask and Flask-RESTX. It implements the Presentation layer (API) and Business Logic layer with an in-memory persistence layer.

## Project Structure
- `run.py` – app entrypoint.
- `config.py` – minimal config stubs.
- `app/`
  - `__init__.py` – Flask app factory; registers API and facade.
  - `api/` – Flask-RESTX setup.
    - `v1/` – Namespaces for users, places, reviews, amenities.
  - `models/` – Domain entities (`User`, `Place`, `Review`, `Amenity`, `BaseModel`).
  - `persistence/` – `InMemoryRepository` generic.
  - `services/` – `HBnBFacade` orchestrating business logic.

## Quickstart
```bash
cd part2
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=run.py
flask run --host=0.0.0.0 --port=8000
```
API docs available at `http://localhost:8000/api/docs`.

## Facade Overview
- Users: register/list/get/update (no delete in API); email uniqueness check.
- Amenities: create/list/get/update (no delete in API).
- Places: create (owner + amenities must exist), list with filters (price range, lat/lng + radius, amenity_ids), get/update (no delete in API).
- Reviews: create (user/place must exist), list/get/update/delete; place average rating computed from reviews.

## Notes / Future Work
- Persistence is in-memory; swap `InMemoryRepository` for real storage later.
- Passwords are stored plaintext for now—replace with hashing when adding auth.
- Distance filter uses a simple Euclidean helper; replace with proper haversine if needed.
- Model-level validation exists but is minimal; extend as needed.
- Deletes are limited by task scope (only reviews have API delete).

## Testing
- Automated: `pytest` from `part2` (uses Flask test client, in-memory data).
- Manual: use `curl` or Swagger UI at `http://localhost:8000/api/docs`.
