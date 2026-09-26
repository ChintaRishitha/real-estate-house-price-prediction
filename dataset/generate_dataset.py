import os
import numpy as np
import pandas as pd

# Create dataset folder if it does not exist
os.makedirs("dataset", exist_ok=True)

# For reproducible results
np.random.seed(42)

# Number of houses
n = 1200

# Locations
locations = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Pune",
    "Delhi",
    "Mumbai",
    "Kolkata"
]

# Location price multipliers
location_multiplier = {
    "Hyderabad": 1.00,
    "Bangalore": 1.15,
    "Chennai": 1.05,
    "Pune": 1.00,
    "Delhi": 1.25,
    "Mumbai": 1.60,
    "Kolkata": 0.90
}

# Generate house features
area = np.random.randint(500, 5001, n)
bedrooms = np.random.randint(1, 7, n)
bathrooms = np.random.randint(1, 6, n)
floors = np.random.randint(1, 5, n)
parking = np.random.randint(0, 5, n)
age = np.random.randint(0, 51, n)
location = np.random.choice(locations, n)

# Calculate base price
base_price = (
    3500 * area
    + 150000 * bedrooms
    + 250000 * bathrooms
    + 300000 * floors
    + 400000 * parking
    - 45000 * age
)

# Apply location premium
price = np.array([
    base_price[i] * location_multiplier[location[i]]
    for i in range(n)
])

# Add random noise
price = price + np.random.normal(0, 250000, n)

# Minimum house price
price = np.maximum(price, 800000)

# Round price to nearest Rs. 1,000
price = np.round(price / 1000) * 1000

# Create DataFrame
df = pd.DataFrame({
    "area": area,
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "floors": floors,
    "parking": parking,
    "age": age,
    "location": location,
    "price": price.astype(int)
})

# Add some missing parking values
missing_indices = np.random.choice(df.index, 15, replace=False)
df.loc[missing_indices, "parking"] = np.nan

# Save dataset
output_file = "dataset/house_prices.csv"
df.to_csv(output_file, index=False)

print("Dataset generated successfully!")
print(f"Number of records: {len(df)}")
print(f"Saved to: {output_file}")
print("\nFirst 5 records:")
print(df.head())