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
    method = "/postcodes"
    full_endpoint = BASE_URL + method
    response = req.get(
        full_endpoint,
        params={
            "lat": lat,
            "lon": long,
        },
        timeout=5,
    )
    print(response.request)
    if response.status_code != 200:
        raise req.RequestException("Unable to access API.")
    closest_code = response.json()["result"]
    if not closest_code:
        raise ValueError("No relevant postcode found.")
    return closest_code[0]["postcode"]


def get_postcode_completions(postcode_start: str) -> list[str]:
    """Obtain possible postcode completions based on the start of a postcode."""
    if not isinstance(postcode_start, str):
        raise TypeError("Function expects a string.")
    method = "/postcodes"
    required_url = f"{BASE_URL}{method}/{postcode_start}/autocomplete"
    response = req.get(required_url)
    if response.status_code >= 300:
        raise req.RequestException("Unable to access API.")
    return response.json()["result"]


def get_postcodes_details(postcodes: list[str]) -> dict:
    if not isinstance(postcodes, list):
        raise TypeError("Function expects a list of strings.")
    for postcode in postcodes:
        if not isinstance(postcode, str):
            print(postcode)
            raise TypeError("Function expects a list of strings.")
    method = "/postcodes"
    response = req.post(
        f"{BASE_URL}{method}",
        headers={"content-type": "application/json"},
        json={"postcodes": postcodes},
        timeout=5,
    )
    if response.status_code >= 300:
        raise req.RequestException("Unable to access API.")
    return response.json()["result"]
