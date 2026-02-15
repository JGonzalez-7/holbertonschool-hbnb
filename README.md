# Holbertonschool HBnB Project

This repository contains the HBnB project deliverables. Part 1 is UML-only; Part 2 is a working Flask API with in-memory persistence based on that design.

## Repository Structure
- `part1/` – UML assets.
  - `high-level_package_diagram.md` – three-layer architecture with Facade.
  - `class_diagram_for_business_logic_layer.md` – core domain class diagram (canonical); `business-logic-layer-class-diagram.md` is a duplicate reference.
  - Sequence diagrams: `user-registration.md`, `place-creation.md`, `review-submission.md`, `fetch-List-of-places.md`.
  - `sequence_diagrams_for_api_calls.md` – aggregated sequence diagrams.
  - `doc_compilation.md` – compiled technical document embedding the diagrams.
  - `README.md` – part-specific guide.
- `part2/hbnb/` – Flask + Flask-RESTX implementation with in-memory repos.
  - `app/` – API namespaces, facade, models, persistence.
  - `run.py` – app entrypoint (`flask run --port 8000`).
  - `tests/` – pytest integration tests.
  - `README.md` – quickstart and feature overview.

## Quickstart (Part 2)
```bash
cd part2/hbnb
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=run.py
flask run --host=0.0.0.0 --port=8000
```
Docs: `http://localhost:8000/api/docs`  
Tests: `pytest`

## Notes
- Diagrams are text-based for version control friendliness.
- Keep `class_diagram_for_business_logic_layer.md` as the single source for the business-logic class diagram to avoid divergence.
- Part 2 uses in-memory storage; swap repos for a DB in later parts.
