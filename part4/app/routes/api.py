"""API proxy routes for the HBnB Part 4 web client."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, current_app, jsonify, request

from app.services.backend import BackendClient, BackendClientError, BackendResponse

api_bp = Blueprint("api_proxy", __name__, url_prefix="/api")


def _backend_client() -> BackendClient:
    client = current_app.extensions.get("backend_client")
    if client is None:
        raise RuntimeError("Backend client not configured")
    return client


def _get_token_from_cookie() -> str | None:
    token = request.cookies.get("token")
    if token is None:
        return None

    token = token.strip()
    return token or None


def _anonymous_session_payload() -> dict[str, Any]:
    return {
        "logged_in": False,
        "user_id": None,
        "is_admin": False,
    }


def _json_error(message: str, status_code: int):
    return jsonify({"message": message}), status_code


def _normalize_upstream_payload(response: BackendResponse) -> Any:
    if response.payload is not None:
        return response.payload
    if response.text:
        return {"message": response.text}
    return ""


def _proxy_response(response: BackendResponse):
    payload = _normalize_upstream_payload(response)
    if payload == "":
        return "", response.status_code
    return jsonify(payload), response.status_code


@api_bp.errorhandler(BackendClientError)
def handle_backend_error(error: BackendClientError):
    """Return a gateway-style response when the backend cannot be reached."""
    return _json_error(str(error), 502)


@api_bp.get("/session")
def get_session_state():
    """Return the current web client session state."""
    token = _get_token_from_cookie()
    if token is None:
        return jsonify(_anonymous_session_payload())

    response = _backend_client().request("GET", "/auth/protected", token=token)
    if response.status_code != 200:
        return jsonify(_anonymous_session_payload())

    payload = response.payload or {}
    return jsonify(
        {
            "logged_in": True,
            "user_id": payload.get("user_id"),
            "is_admin": bool(payload.get("is_admin", False)),
        }
    )


@api_bp.post("/session/login")
def login():
    """Authenticate against the Part 3 backend and store the token in the session."""
    payload = request.get_json(silent=True) or {}
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))

    if not email or not password:
        return _json_error("email and password are required", 400)

    backend = _backend_client()
    login_response = backend.request(
        "POST",
        "/auth/login",
        json={"email": email, "password": password},
    )
    if login_response.status_code != 200:
        return _proxy_response(login_response)

    access_token = (login_response.payload or {}).get("access_token")
    if not access_token:
        return _json_error("Backend login response did not include an access token", 502)

    protected_response = backend.request("GET", "/auth/protected", token=access_token)
    if protected_response.status_code != 200:
        return _json_error("Failed to verify the authenticated session", 502)

    protected_payload = protected_response.payload or {}
    return jsonify(
        {
            "access_token": access_token,
            "logged_in": True,
            "user_id": protected_payload.get("user_id"),
            "is_admin": bool(protected_payload.get("is_admin", False)),
        }
    )


@api_bp.post("/session/logout")
def logout():
    """Clear the local web client session."""
    response = jsonify({"message": "Logged out"})
    response.delete_cookie("token", path="/")
    return response


@api_bp.get("/places")
def list_places():
    """Proxy the public places listing."""
    return _proxy_response(_backend_client().request("GET", "/places/"))


@api_bp.get("/places/<string:place_id>")
def get_place(place_id: str):
    """Proxy a public place detail request."""
    return _proxy_response(_backend_client().request("GET", f"/places/{place_id}"))


@api_bp.get("/amenities")
def list_amenities():
    """Proxy the public amenities listing."""
    return _proxy_response(_backend_client().request("GET", "/amenities/"))


@api_bp.get("/users/<string:user_id>")
def get_user(user_id: str):
    """Proxy a public user detail request."""
    return _proxy_response(_backend_client().request("GET", f"/users/{user_id}"))


@api_bp.post("/reviews")
def create_review():
    """Proxy authenticated review creation using the session token."""
    access_token = _get_token_from_cookie()
    if not access_token:
        return _json_error("Authentication required", 401)

    payload = request.get_json(silent=True) or {}
    return _proxy_response(
        _backend_client().request(
            "POST",
            "/reviews/",
            token=str(access_token),
            json=payload,
        )
    )


__all__ = ["api_bp"]
