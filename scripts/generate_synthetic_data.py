"""
Script to generate synthetic restaurant data for testing
"""

import pandas as pd
import random
from pathlib import Path

# Cities and locations
cities = {
    "Bangalore": ["Indiranagar", "Koramangala", "MG Road", "Whitefield", "HSR Layout"],
    "Delhi": ["Connaught Place", "Hauz Khas", "Saket", "Rajouri Garden", "Vasant Kunj"],
    "Mumbai": ["Bandra", "Andheri", "Colaba", "Juhu", "Powai"],
    "Chennai": ["T Nagar", "Adyar", "Besant Nagar", "Nungambakkam", "Velachery"],
    "Hyderabad": ["Banjara Hills", "Jubilee Hills", "Gachibowli", "Madhapur", "Secunderabad"],
}

# Cuisines
cuisines_list = [
    ["Italian", "Continental"],
    ["North Indian", "Mughlai"],
    ["South Indian"],
    ["Chinese", "Thai"],
    ["Mexican"],
    ["Japanese", "Sushi"],
    ["French"],
    ["American", "Burgers"],
    ["Indian", "Chinese"],
    ["Arabic", "Lebanese"],
]

# Restaurant name prefixes and suffixes
prefixes = ["The", "Royal", "Grand", "Spice", "Taste", "Flavors", "Kitchen", "Bistro", "Cafe", "House"]
suffixes = ["Hub", "Corner", "Garden", "Paradise", "Palace", "Junction", "Point", "Square", "Central", "Lounge"]

# Generate restaurants
restaurants = []
restaurant_id = 1

for city, locations in cities.items():
    for location in locations:
        # Generate 3-5 restaurants per location
        num_restaurants = random.randint(3, 5)
        
        for _ in range(num_restaurants):
            # Generate name
            name = f"{random.choice(prefixes)} {random.choice(cuisines_list)[0]} {random.choice(suffixes)}"
            
            # Generate cuisines
            cuisines = random.choice(cuisines_list)
            
            # Generate rating (skewed towards higher ratings)
            rating = round(random.uniform(3.0, 5.0), 1)
            
            # Generate cost based on budget band
            budget_bands = ["low", "medium", "high"]
            budget_band = random.choice(budget_bands)
            
            if budget_band == "low":
                cost = random.randint(200, 500)
            elif budget_band == "medium":
                cost = random.randint(600, 1500)
            else:
                cost = random.randint(1600, 3000)
            
            # Generate ID
            location_clean = location.lower().replace(" ", "-")
            name_clean = name.lower().replace(" ", "-")
            restaurant_id_str = f"{location_clean}-{name_clean}-{restaurant_id}"
            
            restaurants.append({
                "name": name,
                "location": f"{location}, {city}",
                "cuisines": cuisines,
                "rating": rating,
                "estimated_cost": cost,
                "budget_band": budget_band,
                "id": restaurant_id_str,
            })
            
            restaurant_id += 1

# Create DataFrame
df = pd.DataFrame(restaurants)

print(f"Generated {len(df)} restaurants")
print(f"Columns: {list(df.columns)}")
print(f"\nSample restaurants:")
print(df.head(10))

# Save to Parquet
output_path = Path("data/processed/restaurants.parquet")
output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_parquet(output_path, index=False)

print(f"\nSaved to: {output_path}")

# Statistics
print(f"\nStatistics:")
print(f"Total restaurants: {len(df)}")
print(f"Cities: {df['location'].apply(lambda x: x.split(', ')[1]).nunique()}")
print(f"Budget distribution:")
print(df['budget_band'].value_counts())
print(f"\nRating distribution:")
print(df['rating'].describe())
