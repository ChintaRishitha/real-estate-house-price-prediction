import os
import pickle
import pandas as pd
import matplotlib

# Use a non-GUI backend for saving charts
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)


# --------------------------------------------------
# 1. Create required folders
# --------------------------------------------------

os.makedirs("model", exist_ok=True)
os.makedirs("charts", exist_ok=True)


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

data_path = "dataset/house_prices.csv"

df = pd.read_csv(data_path)

print("Dataset loaded successfully!")
print("Number of records:", len(df))


# --------------------------------------------------
# 3. Remove duplicate records
# --------------------------------------------------

df = df.drop_duplicates()


# --------------------------------------------------
# 4. Handle missing values
# --------------------------------------------------

# Fill missing parking values with the mode
df["parking"] = df["parking"].fillna(df["parking"].mode()[0])

# Remove any remaining missing values
df = df.dropna()


# --------------------------------------------------
# 5. Select features and target
# --------------------------------------------------

features = [
    "area",
    "bedrooms",
    "bathrooms",
    "floors",
    "parking",
    "age",
    "location"
]

target = "price"

X = df[features]
y = df[target]


# --------------------------------------------------
# 6. Define numerical and categorical features
# --------------------------------------------------

numeric_features = [
    "area",
    "bedrooms",
    "bathrooms",
    "floors",
    "parking",
    "age"
]

categorical_features = [
    "location"
]


# --------------------------------------------------
# 7. Preprocessing
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# --------------------------------------------------
# 8. Create Multiple Linear Regression model
# --------------------------------------------------

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ]
)


# --------------------------------------------------
# 9. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print("Training records:", len(X_train))
print("Testing records:", len(X_test))


# --------------------------------------------------
# 10. Train the model
# --------------------------------------------------

print("\nTraining Multiple Linear Regression model...")

model.fit(X_train, y_train)

print("Model training completed!")


# --------------------------------------------------
# 11. Make predictions
# --------------------------------------------------

y_pred = model.predict(X_test)


# --------------------------------------------------
# 12. Calculate performance metrics
# --------------------------------------------------

r2 = r2_score(y_test, y_pred)

mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = mse ** 0.5


print("\nModel Performance")
print("--------------------------")
print(f"R2 Score : {r2:.4f}")
print(f"MAE      : ₹{mae:,.2f}")
print(f"MSE      : {mse:,.2f}")
print(f"RMSE     : ₹{rmse:,.2f}")


# --------------------------------------------------
# 13. Save model
# --------------------------------------------------

model_path = "model/house_price_model.pkl"

with open(model_path, "wb") as file:
    pickle.dump(model, file)

print("\nModel saved to:", model_path)


# --------------------------------------------------
# 14. Save preprocessing object
# --------------------------------------------------

preprocessor_path = "model/preprocessor.pkl"

with open(preprocessor_path, "wb") as file:
    pickle.dump(preprocessor, file)

print("Preprocessor saved to:", preprocessor_path)


# --------------------------------------------------
# 15. Save metrics
# --------------------------------------------------

metrics = {
    "r2": r2,
    "mae": mae,
    "mse": mse,
    "rmse": rmse,
    "records": len(df),
    "features": len(features)
}

metrics_path = "model/metrics.pkl"

with open(metrics_path, "wb") as file:
    pickle.dump(metrics, file)

print("Metrics saved to:", metrics_path)


# --------------------------------------------------
# 16. Chart 1 - Actual vs Predicted Prices
# --------------------------------------------------

plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    y_pred,
    alpha=0.6
)

min_value = min(y_test.min(), y_pred.min())
max_value = max(y_test.max(), y_pred.max())

plt.plot(
    [min_value, max_value],
    [min_value, max_value],
    linestyle="--"
)

plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")

plt.title("Actual vs Predicted House Prices")

plt.tight_layout()

plt.savefig(
    "charts/actual_vs_predicted.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 17. Chart 2 - Price by Location
# --------------------------------------------------

location_prices = df.groupby("location")["price"].mean().sort_values()

plt.figure(figsize=(9, 6))

location_prices.plot(kind="bar")

plt.xlabel("Location")
plt.ylabel("Average House Price")

plt.title("Average House Price by Location")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "charts/price_by_location.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 18. Chart 3 - Area vs Price
# --------------------------------------------------

plt.figure(figsize=(8, 6))

plt.scatter(
    df["area"],
    df["price"],
    alpha=0.5
)

plt.xlabel("Area (sq ft)")
plt.ylabel("House Price")

plt.title("Area vs House Price")

plt.tight_layout()

plt.savefig(
    "charts/area_vs_price.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 19. Completion message
# --------------------------------------------------

print("\n----------------------------------------")
print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
print("----------------------------------------")

print("\nGenerated files:")

print("1. model/house_price_model.pkl")
print("2. model/preprocessor.pkl")
print("3. model/metrics.pkl")
print("4. charts/actual_vs_predicted.png")
print("5. charts/price_by_location.png")
print("6. charts/area_vs_price.png")