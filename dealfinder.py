import os
import json
import requests
import googlemaps
import re
from typing import List, Dict, Optional
from dataclasses import dataclass, field

# --- CONFIGURATION ---

# 1. Serper API Key (from you) for Google Shopping search
SERPER_API_KEY = "ef77c1481fbec9baad24a5a4bae00e76b982e10f"

# 2. Google Maps API Key (from your previous code)
#    You MUST enable these 3 APIs in your Google Cloud project:
#    - Geocoding API
#    - Places API
#    - Distance Matrix API
GOOGLE_MAPS_API_KEY = "AIzaSyD4t3RmmWjENJgWyeLo-qx5I0GRXbQUDxY"


# Initialize Google Maps client
if not GOOGLE_MAPS_API_KEY:
    print("Error: GOOGLE_MAPS_API_KEY not set.")
    exit()

try:
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
except Exception as e:
    print(f"Error initializing Google Maps. Is your API key valid? {e}")
    exit()

# --- DATA CLASSES ---


@dataclass
class Deal:
    product_name: str
    price_str: str
    price_float: float
    store_name: str
    product_link: str
    snippet: Optional[str] = None  # For quantity/unit info

    # Info to be added later
    store_address: Optional[str] = None
    store_maps_link: Optional[str] = None
    distance: Optional[str] = None
    duration: Optional[str] = None


# --- API FUNCTIONS ---


def get_location_details(location_string: str) -> Optional[Dict]:
    """Converts a string location (e.g., "College Park, MD") into coordinates."""
    print(f"\n📍 Geocoding location: '{location_string}'...")
    try:
        geocode_result = gmaps.geocode(location_string)
        if not geocode_result:
            print(f"Error: Could not find location '{location_string}'")
            return None

        loc = geocode_result[0]["geometry"]["location"]
        address = geocode_result[0]["formatted_address"]
        print(f"   -> Found: {address}")
        return {
            "lat": loc["lat"],
            "lng": loc["lng"],
            "address": address,
            "coords_str": f"{loc['lat']},{loc['lng']}",
        }
    except Exception as e:
        print(f"   -> Google Geocoding API Error: {e}")
        return None


def get_google_shopping_deals(product_name: str, location_address: str) -> List[Deal]:
    """Gets product deals from Google Shopping via Serper API."""
    print(f"\n🔎 Searching Google Shopping for '{product_name}'...")

    url = "https://google.serper.dev/shopping"
    payload = json.dumps(
        {
            "q": product_name,
            "location": location_address,  # Use full address for accurate local results
            "num": 15,  # Get 15 results to find good ones
        }
    )
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        deals = []
        for item in data.get("shopping", []):
            # Filter out bad data (no price, no store)
            if not item.get("price") or not item.get("source"):
                continue

            # Extract float from price string like "$5.99"
            price_float = float(re.sub(r"[^\d.]", "", item.get("price", "0")))
            if price_float == 0:
                continue

            deals.append(
                Deal(
                    product_name=item.get("title"),
                    price_str=item.get("price"),
                    price_float=price_float,
                    store_name=item.get("source"),
                    product_link=item.get("link"),
                    snippet=item.get("snippet"),
                )
            )

        # Sort by cheapest and return top 7
        deals.sort(key=lambda x: x.price_float)
        print(f"   -> Found {len(deals)} valid deals.")
        return deals[:7]

    except Exception as e:
        print(f"   -> Serper API Error: {e}")
        return []


# Cache to avoid duplicate API calls for the same store
store_location_cache = {}


def find_nearest_store_and_travel(deal: Deal, user_coords: str, user_lat_lng: Dict):
    """
    Finds the nearest physical store for a deal and gets its address
    and travel time.
    """
    store_name = deal.store_name

    # Check cache first
    if store_name in store_location_cache:
        print(f"   -> Found '{store_name}' in cache.")
        cached_info = store_location_cache[store_name]
        deal.store_address = cached_info.get("address")
        deal.store_maps_link = cached_info.get("maps_link")
        deal.distance = cached_info.get("distance")
        deal.duration = cached_info.get("duration")
        return

    print(f"   -> Finding nearest physical store for '{store_name}'...")

    try:
        # 1. Find nearest store (Places API)
        places_result = gmaps.places_nearby(
            location=(user_lat_lng["lat"], user_lat_lng["lng"]),
            keyword=store_name,
            rank_by="distance",  # CRITICAL: finds the closest one
            type="grocery_or_supermarket",
        )

        if not places_result.get("results"):
            print(f"     Could not find a physical location for '{store_name}'.")
            store_location_cache[store_name] = {}  # Cache the failure
            return

        closest_store = places_result["results"][0]
        store_address = closest_store.get("vicinity")
        store_place_id = closest_store.get("place_id")
        store_maps_link = (
            f"https://www.google.com/maps/place/?q=place_id:{store_place_id}"
        )

        # 2. Find travel time (Distance Matrix API)
        matrix = gmaps.distance_matrix(
            origins=[user_coords],
            destinations=[f"place_id:{store_place_id}"],
            mode="driving",
        )

        distance = "N/A"
        duration = "N/A"
        if matrix["rows"][0]["elements"][0]["status"] == "OK":
            distance = matrix["rows"][0]["elements"][0]["distance"]["text"]
            duration = matrix["rows"][0]["elements"][0]["duration"]["text"]

        # 3. Update the deal and the cache
        deal.store_address = store_address
        deal.store_maps_link = store_maps_link
        deal.distance = distance
        deal.duration = duration

        store_location_cache[store_name] = {
            "address": store_address,
            "maps_link": store_maps_link,
            "distance": distance,
            "duration": duration,
        }

    except Exception as e:
        print(f"     -> Google Maps Error for '{store_name}': {e}")
        store_location_cache[store_name] = {}  # Cache the failure


# --- MAIN EXECUTION ---


def main():
    # --- 1. SET INPUTS ---
    product_to_search = "eggs"
    user_location_string = "College Park, MD 20740"

    print(f"=== 🛒 Smart Shopper Prototype ===")

    # --- 2. GET USER LOCATION ---
    location_details = get_location_details(user_location_string)
    if not location_details:
        return

    # --- 3. GET DEALS ---
    deals = get_google_shopping_deals(
        product_to_search,
        location_details["address"],  # Use full address for better shopping results
    )

    if not deals:
        print("\nNo product deals found. Check your Serper API key or search term.")
        return

    print("\n🚚 Fetching nearest store locations and travel times...")

    # --- 4. ENRICH DEALS (Find nearest store + travel) ---
    for deal in deals:
        find_nearest_store_and_travel(
            deal,
            location_details["coords_str"],
            {"lat": location_details["lat"], "lng": location_details["lng"]},
        )

    # --- 5. DISPLAY RESULTS ---
    print("\n\n--- 🏆 TOP 7 CHEAPEST DEALS ---")
    for i, deal in enumerate(deals, 1):
        print(f"\n{i}. {deal.product_name}")
        print(f"   Price:   {deal.price_str} (from {deal.store_name})")

        if deal.snippet:
            # Clean up the snippet
            snippet_clean = deal.snippet.replace("\n", " ").strip()
            print(f"   Info:    {snippet_clean}")

        if deal.store_address:
            print(f"   Nearest: {deal.store_address}")
            print(f"   Travel:  {deal.distance} ({deal.duration} by car)")
            print(f"   Maps:    {deal.store_maps_link}")
        else:
            print(f"   Store:   Online or local address not found")

        print(f"   Product: {deal.product_link}")


if __name__ == "__main__":
    main()
