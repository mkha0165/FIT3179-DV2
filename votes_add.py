import pandas as pd

# Read with fallback encoding
movies = pd.read_csv('movies.csv', encoding='utf-8')
stats = pd.read_csv('key2stats_movies.csv', encoding='latin1')  # Fix here

# Adjust the key name if necessary
merged = pd.merge(movies, stats[['name', 'votes']], on='name', how='left')

# Save updated file
merged.to_csv('movies_merged.csv', index=False, encoding='utf-8')

print("Added 'votes' column and saved to movies_merged.csv")
