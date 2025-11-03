# Category --> General Track

🛒 Smart Shopper

A simple web app to find the cheapest and closest stores for a grocery item, designed for users in new neighborhoods.

Inspiration

When we first moved to a new area, we were clueless about where to shop. We often chose the most expensive or farthest stores simply because we didn't know better. We built this app to solve that problem—to help anyone new to a locality find the most affordable and convenient places to buy their daily needs.

Features

Price Comparison: Finds the top 4-7 cheapest deals for a product (e.g., "Milk") by searching Google Shopping.

Store Localization: For each deal, it finds the nearest physical store location.

Travel Integration: Calculates the real-world driving distance and travel time to that specific store.

All-in-One Results: Displays a clean, sorted list showing the product, price, store name, store address, and travel time, with hyperlinks to the product page and Google Maps.

Tech Stack

Backend: Python 3, Flask

APIs:

Serper API: (Google Shopping) for product names, prices, and store names.

Google Maps Geocoding API: To convert a user's location string into coordinates.

Google Maps Places API: To find the nearest physical store address.

Google Maps Distance Matrix API: To calculate travel time and distance.

Frontend: HTML, Tailwind CSS, JavaScript (Fetch API)

How It Works (Architecture)

User Input: A user enters a product ("Milk") and a location ("College Park, MD").

Geocode: The location string is sent to the Google Geocoding API to get precise latitude/longitude coordinates.

Fetch Deals: The product name and location are sent to the Serper (Google Shopping) API, which returns a list of products, prices, and store names (e.g., "Target", "Safeway").

Find Nearest Stores: The app loops through each unique store name. It uses the Google Places API to find the single closest store (e.g., "Target") to the user's coordinates.

Calculate Travel: The Google Distance Matrix API is called to get the driving time and distance from the user to that specific store.

Display Results: The final, combined list is sent to the frontend and displayed to the user, sorted by cheapest price.

How to Run Locally

Clone the Repository:

git clone [https://github.com/your-username/smart-shopper.git](https://github.com/your-username/smart-shopper.git)
cd smart-shopper


Install Dependencies:

pip install -r requirements.txt


Set API Keys:
You must get API keys and set them as environment variables.

Serper API: Get from serpapi.com

Google Maps API: Get from Google Cloud Console. You must enable:

Geocoding API

Places API

Distance Matrix API

# On macOS/Linux
export SERPAPI_API_KEY="your_serper_key_here"
export GOOGLE_MAPS_API_KEY="your_google_key_here"

# On Windows (PowerShell)
$env:SERPAPI_API_KEY="your_serper_key_here"
$env:GOOGLE_MAPS_API_KEY="your_google_key_here"


Run the Server:

python app.py


Open the App:
Visit http://127.0.0.1:5001 in your web browser.

Key Learnings

Our biggest challenge was finding a reliable, real-time data source.

Web Scraping is Brittle: We first tried scraping websites with Selenium, but this was slow, error-prone, and broke every time a site's HTML changed.

Generative AI Can Hallucinate: We then tried using a Generative AI to parse HTML, but it often "hallucinated" incorrect prices or broken links, which was impossible to debug.

Structured APIs are the Solution: We learned that for time-sensitive, structured data (like prices and locations), using robust, documented APIs (like Serper and Google Maps) is the correct approach. It's faster, 100% reliable, and led to a cleaner, more professional, and maintainable project.
