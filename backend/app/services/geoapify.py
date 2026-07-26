import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEOAPIFY_API_KEY")

GEOCODE_URL = "https://api.geoapify.com/v1/geocode/search"
PLACES_URL = "https://api.geoapify.com/v2/places"


def get_restaurants(city: str, limit: int = 100):
    """
    Fetch restaurants for a city/locality using Geoapify.
    Searches restaurants around the searched location and
    filters them to return only those belonging to the locality.
    """

    # -------------------------
    # Step 1: Geocode the place
    # -------------------------

    geo_response = requests.get(
        GEOCODE_URL,
        params={
            "text": city,
            "limit": 1,
            "apiKey": API_KEY
        },
        timeout=30
    )

    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data.get("features"):
        return []

    feature = geo_data["features"][0]

    # Coordinates of searched place
    lon, lat = feature["geometry"]["coordinates"]

    # -------------------------
    # Step 2: Search restaurants
    # -------------------------

    radius = 10000  # 10 km

    response = requests.get(
        PLACES_URL,
        params={
            "categories": "catering.restaurant",
            "filter": f"circle:{lon},{lat},{radius}",
            "limit": 500,  # Fetch more results before filtering
            "apiKey": API_KEY
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    restaurants = []

    search = city.lower().strip()

    for item in data.get("features", []):

        prop = item.get("properties", {})

        # -------------------------
        # Locality Filtering
        # -------------------------

        print("------------------------")
        print("Search:", search)
        print("Suburb:", prop.get("suburb"))
        print("District:", prop.get("district"))
        print("City:", prop.get("city"))
        print("Formatted:", prop.get("formatted"))

        search_fields = [
            prop.get("suburb", ""),
            prop.get("district", ""),
            prop.get("city", ""),
            prop.get("county", ""),
            prop.get("state_district", ""),
            prop.get("formatted", "")
        ]

        matches = any(
            search in str(field).lower()
            for field in search_fields
        )

        if not matches:
            continue

        # -------------------------
        # Cuisine
        # -------------------------

        cuisine = prop.get("catering", {}).get("cuisine", "")

        if isinstance(cuisine, list):
            cuisine = ", ".join(cuisine)

        if not cuisine:
            cuisine = "-"

        # -------------------------
        # Phone
        # -------------------------

        phone = prop.get("contact", {}).get("phone", "-")

        # -------------------------
        # Coordinates
        # -------------------------

        lat = prop.get("lat")
        lon = prop.get("lon")

        restaurants.append({
            "name": prop.get("name", "N/A"),
            "phone": phone,
            "address": prop.get("formatted", "-"),
            "cuisine": cuisine,
            "google_maps": f"https://www.google.com/maps?q={lat},{lon}"
        })

        # Stop after collecting requested number
        if len(restaurants) >= limit:
            break

    print(f"Geoapify returned: {len(data.get('features', []))} restaurants")
    print(f"Restaurants after filtering: {len(restaurants)}")

    return restaurants