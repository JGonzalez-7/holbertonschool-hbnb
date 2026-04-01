"""Page routes for the HBnB Part 4 web client."""

from __future__ import annotations

from flask import Blueprint, current_app, redirect, render_template, request, url_for

from app.services.backend import BackendResponse

web_bp = Blueprint("web", __name__)


def _session_payload() -> dict[str, object]:
    token = request.cookies.get("token", "").strip()
    if not token:
        return {"logged_in": False, "is_admin": False, "user_id": None}

    backend_client = current_app.extensions.get("backend_client")
    if backend_client is None:
        return {"logged_in": False, "is_admin": False, "user_id": None}

    response = backend_client.request("GET", "/auth/protected", token=token)
    if not isinstance(response, BackendResponse) or response.status_code != 200:
        return {"logged_in": False, "is_admin": False, "user_id": None}

    payload = response.payload or {}
    return {
        "logged_in": True,
        "is_admin": bool(payload.get("is_admin", False)),
        "user_id": payload.get("user_id"),
    }


@web_bp.get("/")
@web_bp.get("/index.html")
def index():
    """Render the home page."""
    return render_template("index.html", page_name="home", page_title="Explore Places")


@web_bp.get("/login")
@web_bp.get("/login.html")
def login():
    """Render the login page."""
    return render_template("login.html", page_name="login", page_title="Sign In")


@web_bp.get("/place.html")
def place_detail():
    """Render the place detail page."""
    return render_template("place.html", page_name="place", page_title="Place Details")


@web_bp.get("/places/<string:place_id>")
def place_detail_legacy(place_id: str):
    """Support the legacy place detail path."""
    return redirect(url_for("web.place_detail", id=place_id))


@web_bp.get("/add_review.html")
def add_review():
    """Render the add review page for authenticated users."""
    if not request.cookies.get("token"):
        return redirect(url_for("web.index"))

    return render_template(
        "add_review.html",
        page_name="add-review",
        page_title="Add Review",
    )


@web_bp.get("/places/<string:place_id>/review")
def add_review_legacy(place_id: str):
    """Support the legacy add review path."""
    return redirect(url_for("web.add_review", id=place_id))


@web_bp.get("/admin/users")
@web_bp.get("/admin/users.html")
def admin_users():
    """Render the administrator user management page."""
    session = _session_payload()
    if not session["logged_in"] or not session["is_admin"]:
        return redirect(url_for("web.index"))

    return render_template(
        "admin_users.html",
        page_name="admin-users",
        page_title="Manage Users",
    )


__all__ = ["web_bp"]
