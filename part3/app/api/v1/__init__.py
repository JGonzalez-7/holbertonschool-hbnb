"""Version 1 REST namespaces for HBnB Part 3."""

from .amenities import api as amenities_api
from .auth import api as auth_api
from .places import api as places_api
from .reviews import api as reviews_api
from .users import api as users_api

namespaces = [users_api, auth_api, amenities_api, places_api, reviews_api]

__all__ = ["namespaces"]
