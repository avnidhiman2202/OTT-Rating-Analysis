
import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_DIR / "dataset"

OUTPUT_DIR = DATASET_DIR / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

csv_files = list(DATASET_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("Original CSV dataset not found!")

csv_file = max(csv_files, key=lambda file: file.stat().st_size)

df = pd.read_csv(csv_file, encoding="utf-8-sig")

original_rows = len(df)

print("=" * 60)
print("          OTT DATA CLEANING PROCESS")
print("=" * 60)

print("\nOriginal dataset:", csv_file.name)
print("Original rows:", original_rows)


# ==========================================
# 2. REMOVE UNNECESSARY COLUMNS
# ==========================================

# Remove automatically generated index column
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

# Remove Type if it contains only one unique value
if "Type" in df.columns and df["Type"].nunique() <= 1:
    df = df.drop(columns=["Type"])


# ==========================================
# 3. CLEAN COLUMN NAMES
# ==========================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("+", "_plus", regex=False)
)


# ==========================================
# 4. CLEAN TEXT COLUMNS
# ==========================================

df["title"] = df["title"].astype("string").str.strip()

df["age"] = (
    df["age"]
    .astype("string")
    .str.strip()
    .replace("", pd.NA)
)

df["age"] = df["age"].fillna("Unknown")


# ==========================================
# 5. CONVERT YEAR INTO NUMERIC FORMAT
# ==========================================

df["year"] = pd.to_numeric(
    df["year"],
    errors="coerce"
)

# Remove records without a valid title or year
df = df.dropna(subset=["title", "year"])

df["year"] = df["year"].astype(int)


# ==========================================
# 6. CLEAN ROTTEN TOMATOES RATINGS
# ==========================================

# Example: "98/100" becomes 98.0

df["rotten_tomatoes"] = (
    df["rotten_tomatoes"]
    .astype("string")
    .str.extract(r"(\d+(?:\.\d+)?)")[0]
)

df["rotten_tomatoes"] = pd.to_numeric(
    df["rotten_tomatoes"],
    errors="coerce"
)

# Valid ratings should be between 0 and 100
df.loc[
    ~df["rotten_tomatoes"].between(0, 100),
    "rotten_tomatoes"
] = np.nan


# ==========================================
# 7. CLEAN PLATFORM COLUMNS
# ==========================================

platform_columns = [
    "netflix",
    "hulu",
    "prime_video",
    "disney_plus"
]

for column in platform_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)

    df[column] = df[column].astype(int)

    df[column] = df[column].clip(0, 1)


# ==========================================
# 8. CHECK DUPLICATES
# ==========================================

# Remove exact duplicate records
df = df.drop_duplicates()

# Check possible repeated titles separately
repeated_titles = df.duplicated(
    subset=["title", "year"],
    keep=False
).sum()


# ==========================================
# 9. CREATE NEW ANALYTICAL COLUMNS
# ==========================================

# Count the number of platforms carrying each title

df["platform_count"] = df[platform_columns].sum(axis=1)

# List platforms for each title

df["available_platforms"] = df.apply(
    lambda row: ", ".join(
        platform.replace("_", " ").title()
        for platform in platform_columns
        if row[platform] == 1
    ),
    axis=1
)

# Add rating category

df["rating_category"] = pd.cut(
    df["rotten_tomatoes"],
    bins=[-1, 39, 59, 79, 100],
    labels=[
        "Low",
        "Average",
        "Good",
        "Excellent"
    ]
)


# ==========================================
# 10. SAVE CLEANED DATASET
# ==========================================

output_file = OUTPUT_DIR / "ott_cleaned.csv"

df.to_csv(output_file, index=False)


# ==========================================
# 11. CLEANING REPORT
# ==========================================

print("\nCLEANING REPORT")
print("-" * 45)

print("Original rows:", original_rows)
print("Final rows:", len(df))
print("Rows removed:", original_rows - len(df))

print("Remaining columns:", len(df.columns))

print(
    "Missing ratings:",
    df["rotten_tomatoes"].isna().sum()
)

print(
    "Unknown age classifications:",
    (df["age"] == "Unknown").sum()
)

print(
    "Repeated title-year records:",
    repeated_titles
)

print(
    "Titles without a listed platform:",
    (df["platform_count"] == 0).sum()
)

print("\nRating categories:")
print(df["rating_category"].value_counts().to_string())

print("\nCleaned dataset saved at:")
print(output_file)

print("\n" + "=" * 60)
print("          DATA CLEANING COMPLETED!")
print("=" * 60)
