import pandas as pd
from pathlib import Path

# Path to data folder
DATA_DIR = Path("data")

# Read all CSV files
csv_files = list(DATA_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("❌ No CSV files found in data/ folder")

dfs = [pd.read_csv(file) for file in csv_files]

# Combine all data
combined_df = pd.concat(dfs, ignore_index=True)

# Normalize product names
combined_df["product"] = combined_df["product"].str.strip().str.lower()

# Filter only Pink Morsel (singular!)
pink_morsels = combined_df[combined_df["product"] == "pink morsel"].copy()

# Clean price column: remove $ and convert to float
pink_morsels["price"] = (
    pink_morsels["price"]
    .str.replace("$", "", regex=False)
    .astype(float)
)

# Calculate sales
pink_morsels["sales"] = pink_morsels["price"] * pink_morsels["quantity"]

# Select final columns
final_df = pink_morsels[["sales", "date", "region"]]

# Save output
output_file = DATA_DIR / "pink_morsels_sales.csv"
final_df.to_csv(output_file, index=False)

print("✅ pink_morsels_sales.csv created successfully!")
