"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"
BASE_URL = "https://api.postcodes.io"


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    ...


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    ...


def validate_postcode(postcode: str) -> bool:
    """Will ascertain if postcode corresponds to a real postcode, based on Postcodes API."""
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")
    method = "/postcodes"
    full_endpoint = BASE_URL + method + "/" + postcode + "/validate"
    response = req.get(full_endpoint, timeout=5)
    if response.status_code == 200:
        return response.json()["result"]
    raise req.RequestException("Unable to access API.")


def get_postcode_for_location(lat: float, long: float) -> str:
    """Get postcode based on a location input"""
    if not isinstance(lat, float) or not isinstance(long, float):
        raise TypeError("Function expects two floats.")
    pass


def get_postcode_completions(postcode_start: str) -> list[str]:
    pass


def get_postcodes_details(postcodes: list[str]) -> dict:
    pass
