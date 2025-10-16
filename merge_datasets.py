import pandas as pd

# Load both datasets
kaggle = pd.read_csv("movies.csv")
key2stats = pd.read_csv("key2stats_movies.csv", encoding="ISO-8859-1")

# Standardize column names
kaggle.columns = kaggle.columns.str.lower()
key2stats.columns = key2stats.columns.str.lower()

key2stats.columns = key2stats.columns.str.strip()
key2stats = key2stats.applymap(lambda x: x.strip() if isinstance(x, str) else x)

kaggle["country"] = kaggle["country"].replace(country_mapping)
key2stats["country"] = key2stats["country"].replace(country_mapping)

# Merge datasets (outer join)
merged = pd.merge(
    kaggle,
    key2stats,
    on=["name", "year", "country"],  # join keys
    how="outer",
    suffixes=("_kaggle", "_key2stats")
)

# Prefer Kaggle values where available
def prefer_kaggle(row, col):
    if pd.notnull(row.get(f"{col}_kaggle")):
        return row[f"{col}_kaggle"]
    return row.get(f"{col}_key2stats")

for col in ["budget", "gross", "genre", "runtime", "score", "company"]:
    merged[col] = merged.apply(lambda r: prefer_kaggle(r, col), axis=1)

# Drop redundant columns
merged = merged.drop(columns=[c for c in merged.columns if c.endswith("_kaggle") or c.endswith("_key2stats")])

# Save merged dataset
merged.to_csv("movies_merged.csv", index=False)

# Build country aggregates for Vega-Lite map
country_agg = merged.groupby("country").agg(
    movie_count=("name", "count"),
    total_gross=("gross", "sum"),
    avg_score=("score", "mean")
).reset_index()

country_agg.to_csv("country_aggregates.csv", index=False)

print("Merged dataset saved as movies_merged.csv")
print("Country aggregates saved as country_aggregates.csv")
