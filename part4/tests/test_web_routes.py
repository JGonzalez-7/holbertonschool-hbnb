"""Page route tests for Part 4."""

from __future__ import annotations


def test_home_page_renders(client):
    response = client.get("/")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Available Places" in body
    assert 'class="logo"' in body
    assert "All rights reserved." in body
    assert 'id="filter"' in body
    assert 'id="price-filter"' in body
    assert 'id="places-list"' in body


def test_login_page_renders(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert "Sign in to HBnB" in response.get_data(as_text=True)


def test_place_page_renders(client):
    response = client.get("/place.html?id=place-1")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Guest feedback" in body
    assert 'id="place-details"' in body
    assert 'id="add-review"' in body
    assert 'id="reviews"' in body


def test_legacy_place_route_redirects_to_query_style_url(client):
    response = client.get("/places/place-1")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/place.html?id=place-1")


def test_add_review_redirects_when_not_authenticated(client):
    response = client.get("/add_review.html?id=place-1")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/index.html")


def test_add_review_page_renders_when_authenticated(client):
    login_response = client.post(
        "/api/session/login",
        json={"email": "user@example.com", "password": "secret123"},
    )
    assert login_response.status_code == 200
    client.set_cookie("token", login_response.get_json()["access_token"])

    response = client.get("/add_review.html?id=place-1")

    assert response.status_code == 200
    assert "Share your stay experience" in response.get_data(as_text=True)


def test_legacy_add_review_route_redirects_to_query_style_url(client):
    response = client.get("/places/place-1/review")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/add_review.html?id=place-1")
