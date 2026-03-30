"""Demo properties and users for the Part 4 web client."""

from __future__ import annotations

from copy import deepcopy


DEMO_USERS = {
    "demo-owner-1": {
        "id": "demo-owner-1",
        "first_name": "Maya",
        "last_name": "Rivera",
        "email": "maya.rivera@example.com",
        "is_admin": False,
    },
    "demo-owner-2": {
        "id": "demo-owner-2",
        "first_name": "Daniel",
        "last_name": "Cruz",
        "email": "daniel.cruz@example.com",
        "is_admin": False,
    },
    "demo-owner-3": {
        "id": "demo-owner-3",
        "first_name": "Elena",
        "last_name": "Lopez",
        "email": "elena.lopez@example.com",
        "is_admin": False,
    },
    "demo-owner-4": {
        "id": "demo-owner-4",
        "first_name": "Luis",
        "last_name": "Martinez",
        "email": "luis.martinez@example.com",
        "is_admin": False,
    },
    "demo-owner-5": {
        "id": "demo-owner-5",
        "first_name": "Camila",
        "last_name": "Soto",
        "email": "camila.soto@example.com",
        "is_admin": False,
    },
    "demo-user-1": {
        "id": "demo-user-1",
        "first_name": "Nina",
        "last_name": "Hart",
        "email": "nina.hart@example.com",
        "is_admin": False,
    },
    "demo-user-2": {
        "id": "demo-user-2",
        "first_name": "Marco",
        "last_name": "Vega",
        "email": "marco.vega@example.com",
        "is_admin": False,
    },
    "demo-user-3": {
        "id": "demo-user-3",
        "first_name": "Sara",
        "last_name": "Dunn",
        "email": "sara.dunn@example.com",
        "is_admin": False,
    },
}


DEMO_PLACES = [
    {
        "id": "demo-place-1",
        "name": "Canopy Loft Retreat",
        "description": "A calm hillside loft with leafy views, a reading nook, and a quiet terrace for slow mornings.",
        "price": 95.0,
        "latitude": 18.343,
        "longitude": -66.114,
        "owner_id": "demo-owner-1",
        "owner": DEMO_USERS["demo-owner-1"],
        "amenities": [
            {"id": "demo-amenity-1", "name": "WiFi"},
            {"id": "demo-amenity-2", "name": "Balcony"},
            {"id": "demo-amenity-3", "name": "Coffee Station"},
        ],
        "reviews": [
            {
                "id": "demo-review-1",
                "rating": 5,
                "comment": "Warm, bright, and surprisingly peaceful.",
                "user_id": "demo-user-1",
                "place_id": "demo-place-1",
            }
        ],
        "average_rating": 5.0,
        "image_url": "/static/images/canopy_loft_retreat.jpg",
        "is_demo": True,
    },
    {
        "id": "demo-place-2",
        "name": "Old Town Courtyard House",
        "description": "A restored house near historic streets with a shaded courtyard and space for long weekend stays.",
        "price": 140.0,
        "latitude": 18.465,
        "longitude": -66.105,
        "owner_id": "demo-owner-2",
        "owner": DEMO_USERS["demo-owner-2"],
        "amenities": [
            {"id": "demo-amenity-4", "name": "Air Conditioning"},
            {"id": "demo-amenity-5", "name": "Patio"},
            {"id": "demo-amenity-6", "name": "Washer"},
        ],
        "reviews": [
            {
                "id": "demo-review-2",
                "rating": 4,
                "comment": "Beautiful location and a very comfortable setup.",
                "user_id": "demo-user-2",
                "place_id": "demo-place-2",
            }
        ],
        "average_rating": 4.0,
        "image_url": "/static/images/old_town_courtyard_house.jpg",
        "is_demo": True,
    },
    {
        "id": "demo-place-3",
        "name": "Ocean Glass Studio",
        "description": "Minimal studio with wide windows, a compact kitchen, and a strong sunset view over the water.",
        "price": 180.0,
        "latitude": 18.377,
        "longitude": -65.958,
        "owner_id": "demo-owner-3",
        "owner": DEMO_USERS["demo-owner-3"],
        "amenities": [
            {"id": "demo-amenity-7", "name": "Ocean View"},
            {"id": "demo-amenity-8", "name": "Kitchen"},
            {"id": "demo-amenity-9", "name": "Workspace"},
        ],
        "reviews": [
            {
                "id": "demo-review-3",
                "rating": 5,
                "comment": "The light in the afternoon makes the whole place glow.",
                "user_id": "demo-user-3",
                "place_id": "demo-place-3",
            }
        ],
        "average_rating": 5.0,
        "image_url": "/static/images/ocean_glass_studio.jpg",
        "is_demo": True,
    },
    {
        "id": "demo-place-4",
        "name": "Garden Patio Bungalow",
        "description": "A low-key bungalow with an outdoor shower, garden seating, and easy access to beach roads.",
        "price": 125.0,
        "latitude": 18.309,
        "longitude": -65.298,
        "owner_id": "demo-owner-4",
        "owner": DEMO_USERS["demo-owner-4"],
        "amenities": [
            {"id": "demo-amenity-10", "name": "Outdoor Shower"},
            {"id": "demo-amenity-11", "name": "Private Parking"},
            {"id": "demo-amenity-12", "name": "BBQ Area"},
        ],
        "reviews": [],
        "average_rating": None,
        "image_url": "/static/images/garden_patio_bungalow.jpg",
        "is_demo": True,
    },
    {
        "id": "demo-place-5",
        "name": "City Roofline Apartment",
        "description": "A polished apartment with a rooftop corner, skyline views, and quick access to dining and nightlife.",
        "price": 210.0,
        "latitude": 18.447,
        "longitude": -66.066,
        "owner_id": "demo-owner-5",
        "owner": DEMO_USERS["demo-owner-5"],
        "amenities": [
            {"id": "demo-amenity-13", "name": "Rooftop Access"},
            {"id": "demo-amenity-14", "name": "Smart TV"},
            {"id": "demo-amenity-15", "name": "Fast WiFi"},
        ],
        "reviews": [
            {
                "id": "demo-review-4",
                "rating": 4,
                "comment": "Great base for exploring the city at night.",
                "user_id": "demo-user-1",
                "place_id": "demo-place-5",
            }
        ],
        "average_rating": 4.0,
        "image_url": "/static/images/city_roofline_apartment.jpg",
        "is_demo": True,
    },
]


def list_demo_places() -> list[dict]:
    """Return demo places as independent dictionaries."""
    return deepcopy(DEMO_PLACES)


def get_demo_place(place_id: str) -> dict | None:
    """Return a demo place by id."""
    for place in DEMO_PLACES:
        if place["id"] == place_id:
            return deepcopy(place)
    return None


def get_demo_user(user_id: str) -> dict | None:
    """Return a demo user by id."""
    user = DEMO_USERS.get(user_id)
    if user is None:
        return None
    return deepcopy(user)


__all__ = ["get_demo_place", "get_demo_user", "list_demo_places"]
