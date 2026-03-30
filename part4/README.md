# HBnB Part 4

Part 4 is a Flask-based web client for the HBnB project. It serves browser pages and proxies selected requests to the Part 3 API while the browser stores the JWT token in a cookie after login.

## Structure
- `app/` Flask application package
- `app/routes/` page routes and API proxy endpoints
- `app/services/` backend API client
- `app/templates/` Jinja templates
- `app/static/` CSS and JavaScript assets
- `tests/` automated tests
- `config.py` environment-specific configuration
- `run.py` development entrypoint

## Quickstart
Start the Part 3 backend first. By default, Part 4 expects the backend at `http://127.0.0.1:8000/api/v1`.

```bash
cd part4
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=run.py
export BACKEND_API_URL=http://127.0.0.1:8000/api/v1
flask run --host=0.0.0.0 --port=5001
```

Open `http://127.0.0.1:5001`.

## User Flows
- Browse places on the home page
- Filter places by maximum price without reloading the page
- Sign in through the Part 3 authentication API and store the JWT in a cookie
- View place details, amenities, owner information, and reviews
- Submit a review for a place while authenticated
- Log out from the web client session

## Testing
Run tests from the `part4` directory:

```bash
pytest
```

## Notes
- The browser never talks directly to the Part 3 API. Part 4 proxies the needed requests through Flask routes under `/api/...`.
- The login flow returns a JWT token, and the frontend stores it in a `token` cookie used for authenticated proxy requests.
- Helper scripts were intentionally omitted from this part.
