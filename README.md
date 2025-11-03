# Category --> General Track


## Inspiration
When we first arrived here as international students from India, we were completely clueless about where to shop. Whether it was milk or a dustbin, we had no idea which stores offered the best prices or were closest to us. More often than not, we ended up choosing the most expensive or farthest option simply because we didn’t know better. We came up with this project to solve that problem — to help new and current students easily find the most affordable and convenient places to buy what they need.

## What it does
In simple terms, our web app helps you find the cheapest and closest options from over 30 nearby stores for any item, like bread, milk, or eggs, based on your location. You can also tell the app how you’ll get there — by walking or driving — and it will suggest the best stores accordingly.

## How we built it
User Input & Location: Users enter a product and location, which is converted to coordinates via Google Geocoding API. Fetch Deals: Serper API retrieves local product deals, filtered and sorted by price. Nearest Stores: Google Places API finds the closest store for each deal. Travel Info: Distance Matrix API calculates travel distance and time. Caching: Store info is cached to reduce repeated API calls. Display: Shows product, price, store, travel info, and links to product/maps. Takeaway: Using robust APIs is faster, more reliable, and easier than web scraping, while giving users price- and distance-optimized shopping recommendations.

## Challenges we ran into
Unreliable Data from Generative AI: Initially, we relied on Gemini APIs to fetch product URLs and pricing. However, the outputs were often hallucinated, showing invalid or broken links. This forced us to carefully debug the issue and ultimately switch to using more reliable APIs like Serper and Google Places. It highlighted the limitations of depending entirely on generative AI for critical data. API Rate Limits & Efficiency: Managing multiple API calls (Google Maps, Distance Matrix, Serper) for dozens of products and stores was challenging. We had to implement caching strategies and optimize queries to avoid exceeding limits while maintaining real-time performance. Data Consistency Across Sources: Prices, availability, and product details varied across stores and data sources. Ensuring consistent, accurate, and comparable information required careful filtering, sorting, and validation of API responses. Distance & Travel Mode Accuracy: Incorporating user-preferred travel modes (walking vs. driving) added complexity. Calculating realistic travel times while matching them with the closest stores required precise integration with Google’s Distance Matrix API. Selenium & Web Scraping Limitations: While Selenium was initially considered for scraping, parsing multiple websites reliably proved extremely error-prone due to inconsistent page structures and dynamic content. This reinforced the decision to rely on well-documented APIs for stability and scalability. Balancing Speed and Reliability: Delivering quick search results while ensuring data accuracy was tricky. Optimizing API calls, caching results, and reducing redundant processing became crucial to provide a smooth user experience.

## Accomplishments that we're proud of
Seamless Price & Distance Optimization: Successfully built a system that recommends stores based on both price and proximity, giving users a practical and cost-effective shopping experience.
Reliable API Integration: Navigated challenges with unreliable data sources and implemented robust APIs (Google Maps, Serper) to provide accurate product listings, prices, and travel info.
Dynamic Travel Mode Handling: Enabled the app to factor in walking vs. driving preferences, making store suggestions more personalized and realistic.
Caching & Performance Optimization: Implemented caching mechanisms to reduce redundant API calls, speeding up response times and improving overall performance.
Proof of Concept Working Across Multiple Items & Stores: Demonstrated that the app can handle searches for various products across more than 30 stores without crashing or showing invalid data.
Debugging & Reliability Achievements: Overcame hallucinations and unreliable URLs from generative AI outputs by systematically validating and filtering results.
User-Centric Design: Focused on making the interface intuitive for students and newcomers, making it easy to search and get actionable results quickly.
Scalable Architecture: Laid the foundation for future features like crowdsourced insights, predictive shopping, and multi-metric recommendations. ## What we learned
Naive coding with generative AI is highly prone to hallucinations and can be difficult to debug. In many cases, it’s more reliable to use conventional, well-documented APIs rather than blindly depending on LLM or GenAI-based solutions. APIs also tend to be faster, more efficient, and easier to integrate compared to traditional parsing tools like Selenium. On a side note, we explored Google Studios as well, but it’s mainly useful for creating generalized front ends and doesn’t handle complex back-end logic well. While we used Selenium extensively, executing parsing reliably across multiple websites proved to be extremely challenging and error-prone.

## What's next for HelpMeShop
We currently have a working proof of concept, but there’s huge potential to make it smarter and more personalized:

Crowdsourced Insights: Aggregate preferences and reviews from users in the same area to recommend stores and products more intelligently.
Multi-Metric Recommendations: Go beyond price — include distance, product quality, user ratings, availability, and even store ambiance.
Dynamic Alerts: Notify users when a favorite item is on sale nearby or if stock is running low at nearby stores.
AI-Powered Suggestions: Suggest alternative products if the exact item isn’t available or if there’s a cheaper/better option.
Route Optimization: For users with multiple items on their list, suggest an optimized shopping route across stores to save time and money.
Personalized Deals & Coupons: Integrate with store promotions or loyalty programs to automatically find the best discounts for the user.
Voice & AR Integration: Let users ask “Where’s the cheapest milk near me?” via voice or see nearby deals through augmented reality on their phone.
Predictive Shopping: Learn shopping habits over time and proactively suggest shopping lists, reminders, or even bundle deals.
