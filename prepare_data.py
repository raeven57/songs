import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the data
df = pd.read_csv('songs_cleaned.csv')

# Normalize the numeric features
scaler = MinMaxScaler()
numeric_features = ['popularity', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
df[numeric_features] = scaler.fit_transform(df[numeric_features])

# Save the processed data
df.to_csv('songs_normalized.csv', index=False)
