import pandas as pd
import re

movies = pd.read_csv("movies_merged.csv")

# Clean up column names
movies.columns = movies.columns.str.strip().str.lower()

# Extract 4-digit year from the "year" column
movies["year_extracted"] = movies["year"].astype(str).str.extract(r"(\d{4})").astype(float)

print("Sample extracted years:")
print(movies[["year", "year_extracted"]].head(10))

for col in movies.columns:
    sample = movies[col].dropna().astype(str).head(10).tolist()
    print(f"{col}: {sample}\n")

# Use fixed year and proper country column
movies["year"] = movies["year_extracted"]
movies["gross"] = pd.to_numeric(movies["gross"], errors="coerce")
movies["score"] = pd.to_numeric(movies["score"], errors="coerce")

# Drop rows missing key data
movies = movies.dropna(subset=["country", "year"])

# Group by country and year
aggregated = (
    movies.groupby(["country", "year"])
    .agg(
        movie_count=("name", "count"),
        total_gross=("gross", "sum"),
        avg_score=("score", "mean")
    )
    .reset_index()
)

aggregated.to_csv("country_aggregates.csv", index=False)
print("Fixed and saved country_aggregates.csv")
