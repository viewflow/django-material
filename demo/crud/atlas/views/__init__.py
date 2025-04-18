"""
Atlas app views package.

This package provides the CRUD views for the Atlas application.
"""

from .city import (
    city_list,
    city_detail, 
    city_create,
    city_update,
    city_delete,
)

from .country import (
    country_list,
    country_detail,
    country_create,
    country_update,
    country_delete,
)

__all__ = [
    'city_list', 'city_detail', 'city_create', 'city_update', 'city_delete',
    'country_list', 'country_detail', 'country_create', 'country_update', 'country_delete',
]