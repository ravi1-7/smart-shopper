# 🛒 Smart Shopper

A web app that finds the cheapest and closest stores for a grocery item, designed for users in new neighborhoods.

## Features

- **Price Comparison**: Finds the top 4-7 cheapest deals from Google Shopping.
- **Store Localization**: For each deal, finds the nearest physical store.
- **Travel Integration**: Calculates the real-world driving distance and time.
- **All-in-One Results**: Displays a sorted list of products, prices, store locations, and travel times with links to the product and maps.

## Tech Stack & Architecture

- **Backend**: Python 3, Flask
- **Frontend**: HTML, Tailwind CSS, JavaScript (Fetch API)

### APIs:

1. **Google Geocoding**: Converts user's location string to coordinates.
2. **Serper API (Google Shopping)**: Fetches product deals (price, name, store).
3. **Google Places API**: Finds the nearest physical store address for each deal.
4. **Google Distance Matrix API**: Calculates travel time and distance.

## How to Run Locally

1. **Clone**:
```bash
   git clone https://github.com/your-username/smart-shopper.git
   cd smart-shopper
```

2. **Install**:
```bash
   pip install -r requirements.txt
```

3. **Set API Keys**: Set `SERPER_API_KEY` and `GOOGLE_MAPS_API_KEY` (with Geocoding, Places, and Distance Matrix APIs enabled) as environment variables:
```bash
   export SERPER_API_KEY="your_serper_key_here"
   export GOOGLE_MAPS_API_KEY="your_google_maps_key_here"
```

4. **Run**:
```bash
   python app.py
```

5. **Open**: Visit `http://127.0.0.1:5000` in your browser.

## Key Learning

Finding a reliable, real-time data source was the biggest challenge. Initial attempts with web scraping (Selenium) were too brittle, and using Generative AI to parse HTML resulted in "hallucinated" or incorrect data. The final, successful solution was to use structured, reliable APIs (Serper and Google Maps), which proved to be faster, more accurate, and more maintainable.