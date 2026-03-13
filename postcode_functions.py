"""Functions that interact with the Postcode API."""

import os
import json
import requests as req


CACHE_FILE = "./postcode_cache.json"
BASE_URL = "https://api.postcodes.io"


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f)


def check_existing_cache():
    """check if a cache exists and if it doesn't create an empty one."""
    if not os.path.exists(CACHE_FILE):
        save_cache({})


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    check_existing_cache()
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def check_cache(cache: dict, postcode: str, key: str) -> bool:
    """Will update a cache will a postcode key if doesn't exist,
    and will give True if the key exists in the dict value of the
    postcode key."""
    if postcode not in cache:
        cache[postcode] = {}
        return False
    if key not in cache[postcode]:
        return False
    return True


def validate_postcode(postcode: str) -> bool:
    """Will ascertain if postcode corresponds to a real postcode, based on Postcodes API."""
    current_cache = load_cache()
    if not isinstance(postcode, str):
        raise TypeError("Function expects a string.")
    if check_cache(current_cache, postcode, "valid"):
        return current_cache[postcode]["valid"]
    method = "/postcodes"
    full_endpoint = BASE_URL + method + "/" + postcode + "/validate"
    response = req.get(full_endpoint, timeout=5)
    if response.status_code >= 300:
        raise req.RequestException("Unable to access API.")
    valid = response.json()["result"]
    current_cache[postcode]["valid"] = valid
    save_cache(current_cache)
    return valid


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
    current_cache = load_cache()
    if check_cache(current_cache, postcode_start, "completions"):
        return current_cache[postcode_start]["completions"]
    method = "/postcodes"
    required_url = f"{BASE_URL}{method}/{postcode_start}/autocomplete"
    response = req.get(required_url, timeout=5)
    if response.status_code >= 300:
        raise req.RequestException("Unable to access API.")
    completions = response.json()["result"]
    current_cache[postcode_start]["completions"] = completions
    save_cache(current_cache)
    return completions


def get_postcodes_details(postcodes: list[str]) -> dict:
    """Obtain details for a range of postcodes as a dictionary for each query."""
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
