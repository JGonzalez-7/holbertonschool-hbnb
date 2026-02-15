"""Version 1 API namespace collection (Flask-RESTX)."""

from .users import api as users_api
from .places import api as places_api
from .reviews import api as reviews_api
from .amenities import api as amenities_api

namespaces = [users_api, places_api, reviews_api, amenities_api]

__all__ = ["namespaces"]
