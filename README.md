# Holbertonschool HBnB Project

This repository contains the HBnB project deliverables across four phases: system design, API implementation, database integration, and a simple web client.

## Repository Structure
- `part1/` – UML assets.
  - `high-level_package_diagram.md` – three-layer architecture with Facade.
  - `class_diagram_for_business_logic_layer.md` – core domain class diagram (canonical); `business-logic-layer-class-diagram.md` is a duplicate reference.
  - Sequence diagrams: `user-registration.md`, `place-creation.md`, `review-submission.md`, `fetch-List-of-places.md`.
  - `sequence_diagrams_for_api_calls.md` – aggregated sequence diagrams.
  - `doc_compilation.md` – compiled technical document embedding the diagrams.
  - `README.md` – part-specific guide.
- `part2/` – Flask + Flask-RESTX API with in-memory persistence.
  - `app/` – API namespaces, facade, models, persistence.
  - `run.py` – app entrypoint (`flask run --port 8000`).
  - `tests/` – pytest integration tests.
  - `README.md` – quickstart and feature overview.
- `part3/` – authenticated Flask API backed by SQLAlchemy and SQLite.
  - `app/` – application package, ORM models, API namespaces, repositories, services.
  - `sql/` – schema, seed, and CRUD verification scripts.
  - `docs/` – ER diagram and supporting documentation.
  - `tests/` – pytest suite for auth, admin access, repository behavior, and API rules.
  - `README.md` – quickstart and database notes.
- `part4/` – Flask-based web client for the Part 3 API.
  - `app/templates/` – login, index, place detail, and add review pages.
  - `app/static/` – CSS, JavaScript, and logo assets.
  - `app/routes/` – web routes and same-origin API proxy routes.
  - `tests/` – pytest suite covering routes and proxy behavior.
  - `README.md` – quickstart and usage notes.

## Quickstart
### Part 2
```bash
cd part2
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=run.py
flask run --host=0.0.0.0 --port=8000
```

Docs: `http://localhost:8000/api/docs`
Tests: `pytest`

### Part 3
```bash
cd part3
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=run.py
flask run --host=0.0.0.0 --port=8000
```

Docs: `http://localhost:8000/api/docs`
Tests: `pytest`

### Part 4
Run the backend and frontend in separate terminals.

Backend terminal:

```bash
cd part3
source venv/bin/activate
export FLASK_APP=run.py
flask run --host=0.0.0.0 --port=8000
```

Frontend terminal:

```bash
cd part4
source .venv/bin/activate
export FLASK_APP=run.py
export BACKEND_API_URL=http://127.0.0.1:8000/api/v1
flask run --host=0.0.0.0 --port=5001
```

Backend API: `http://127.0.0.1:8000/api/v1/places/`
Backend docs: `http://127.0.0.1:8000/api/docs`
Web client: `http://127.0.0.1:5001`
Tests: `pytest`

If the virtual environments do not exist yet:

```bash
cd part3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../part4
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Notes
- Diagrams are text-based for version control friendliness.
- Keep `class_diagram_for_business_logic_layer.md` as the single source for the business-logic class diagram to avoid divergence.
- Part 2 uses in-memory storage.
- Part 3 introduces JWT authentication and relational database persistence.
- Part 4 consumes the Part 3 API through a Flask-served web client.
