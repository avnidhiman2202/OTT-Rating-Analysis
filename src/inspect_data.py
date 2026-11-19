
import pandas as pd
from pathlib import Path

# ==========================================
# 1. FIND AND LOAD THE DATASET
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = PROJECT_DIR / "dataset"

csv_files = list(DATASET_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        "No CSV file found inside the dataset folder!"
    )

csv_file = max(csv_files, key=lambda file: file.stat().st_size)

try:
    df = pd.read_csv(csv_file, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(csv_file, encoding="latin1")

print("\n" + "=" * 60)
print("       OTT RATING ANALYSIS - DATA INSPECTION")
print("=" * 60)

print("\nDataset loaded:", csv_file.name)


# ==========================================
# 2. DATASET DIMENSIONS
# ==========================================

print("\n1. DATASET DIMENSIONS")
print("-" * 40)

print("Total rows:", df.shape[0])
print("Total columns:", df.shape[1])


# ==========================================
# 3. COLUMN INFORMATION
# ==========================================

print("\n2. COLUMN NAMES AND DATA TYPES")
print("-" * 40)

for column in df.columns:
    print(f"{column} : {df[column].dtype}")


# ==========================================
# 4. FIRST FIVE RECORDS
# ==========================================

print("\n3. FIRST FIVE RECORDS")
print("-" * 40)

print(df.head().to_string())


# ==========================================
# 5. MISSING VALUES
# ==========================================

print("\n4. MISSING VALUES")
print("-" * 40)

missing_data = pd.DataFrame({
    "Missing Count": df.isnull().sum(),
    "Missing Percentage": (
        df.isnull().mean() * 100
    ).round(2)
})

print(missing_data.to_string())


# ==========================================
# 6. DUPLICATE RECORDS
# ==========================================

print("\n5. DUPLICATE RECORDS")
print("-" * 40)

print("Duplicate rows:", df.duplicated().sum())


# ==========================================
# 7. STATISTICAL SUMMARY
# ==========================================

print("\n6. NUMERICAL STATISTICS")
print("-" * 40)

print(df.describe().to_string())


# ==========================================
# 8. OTT PLATFORM DISTRIBUTION
# ==========================================

print("\n7. OTT PLATFORM DISTRIBUTION")
print("-" * 40)

platforms = [
    "Netflix",
    "Hulu",
    "Prime Video",
    "Disney+"
]

for platform in platforms:

    if platform in df.columns:

        total = df[platform].eq(1).sum()

        print(f"{platform}: {total} titles")


# ==========================================
# 9. RATING INFORMATION
# ==========================================

print("\n8. RATING INFORMATION")
print("-" * 40)

for column in df.columns:

    if any(
        word in column.lower()
        for word in ["imdb", "rating", "tomato"]
    ):

        print(f"\nColumn: {column}")

        print(df[column].describe())


# ==========================================
# 10. COMPLETION
# ==========================================

print("\n" + "=" * 60)
print("       DATA INSPECTION COMPLETED!")
print("=" * 60)
