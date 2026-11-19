
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "dataset" / "processed" / "ott_cleaned.csv"

OUTPUT_DIR = PROJECT_DIR / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# 2. LOAD CLEANED DATA
# --------------------------------------------------

df = pd.read_csv(DATA_FILE)

print("\n" + "=" * 55)
print("           OTT DATA ANALYSIS")
print("=" * 55)

print("\nDataset shape:", df.shape)


# --------------------------------------------------
# 3. BASIC STATISTICS
# --------------------------------------------------

print("\nBASIC STATISTICS")
print("-" * 40)

print("Total movies:", len(df))

print("Average Rotten Tomatoes rating:",
      round(df["rotten_tomatoes"].mean(), 2))

print("Oldest movie year:", df["year"].min())

print("Latest movie year:", df["year"].max())

print("Movies with ratings:",
      df["rotten_tomatoes"].notna().sum())


# --------------------------------------------------
# 4. PLATFORM ANALYSIS
# --------------------------------------------------

platforms = {
    "Netflix": "netflix",
    "Hulu": "hulu",
    "Prime Video": "prime_video",
    "Disney+": "disney_plus"
}

print("\nPLATFORM ANALYSIS")
print("-" * 40)

platform_results = []

for platform_name, column in platforms.items():

    platform_movies = df[df[column] == 1]

    average_rating = platform_movies["rotten_tomatoes"].mean()

    platform_results.append({
        "Platform": platform_name,
        "Movies": len(platform_movies),
        "Average Rating": round(average_rating, 2)
    })

    print(
        f"{platform_name}: "
        f"{len(platform_movies)} movies | "
        f"Average rating: {average_rating:.2f}"
    )

platform_df = pd.DataFrame(platform_results)


# --------------------------------------------------
# 5. MOVIE RELEASE YEAR ANALYSIS
# --------------------------------------------------

year_counts = df["year"].value_counts().sort_index()

print("\nTOP 10 RELEASE YEARS")
print("-" * 40)

print(year_counts.sort_values(ascending=False).head(10))


# --------------------------------------------------
# 6. RATING CATEGORY ANALYSIS
# --------------------------------------------------

print("\nRATING CATEGORY DISTRIBUTION")
print("-" * 40)

print(df["rating_category"].value_counts())


# --------------------------------------------------
# 7. AGE CLASSIFICATION ANALYSIS
# --------------------------------------------------

print("\nAGE CLASSIFICATION DISTRIBUTION")
print("-" * 40)

print(df["age"].value_counts().head(10))


# --------------------------------------------------
# 8. VISUALIZATION SETTINGS
# --------------------------------------------------

sns.set_theme(style="whitegrid")


# CHART 1: Rating distribution

plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="rotten_tomatoes",
    bins=20,
    kde=True
)

plt.title("Distribution of Rotten Tomatoes Ratings")
plt.xlabel("Rotten Tomatoes Score")
plt.ylabel("Number of Movies")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "rating_distribution.png")

plt.close()


# CHART 2: Movies available on each platform

plt.figure(figsize=(9, 5))

sns.barplot(
    data=platform_df,
    x="Platform",
    y="Movies"
)

plt.title("Movies Available on Each OTT Platform")
plt.xlabel("OTT Platform")
plt.ylabel("Number of Movies")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "platform_movie_count.png")

plt.close()


# CHART 3: Average rating by platform

plt.figure(figsize=(9, 5))

sns.barplot(
    data=platform_df,
    x="Platform",
    y="Average Rating"
)

plt.title("Average Rotten Tomatoes Rating by Platform")
plt.xlabel("OTT Platform")
plt.ylabel("Average Rating")

plt.ylim(0, 100)

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "platform_average_rating.png")

plt.close()


# CHART 4: Movies released by year

plt.figure(figsize=(12, 5))

sns.lineplot(
    x=year_counts.index,
    y=year_counts.values
)

plt.title("Movies Released Over the Years")
plt.xlabel("Release Year")
plt.ylabel("Number of Movies")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "movies_by_year.png")

plt.close()


# CHART 5: Rating categories

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="rating_category",
    order=["Low", "Average", "Good", "Excellent"]
)

plt.title("Movie Rating Categories")
plt.xlabel("Rating Category")
plt.ylabel("Number of Movies")

plt.tight_layout()

plt.savefig(OUTPUT_DIR / "rating_categories.png")

plt.close()


# --------------------------------------------------
# 9. FINAL REPORT
# --------------------------------------------------

print("\n" + "=" * 55)
print("          ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 55)

print("\nFive visualizations saved in:")
print(OUTPUT_DIR)

print("\nFiles created:")
for file in OUTPUT_DIR.glob("*.png"):
    print("-", file.name)
