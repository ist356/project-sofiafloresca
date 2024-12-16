import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Movie Suggester")
st.write("Welcome to the Movie Suggester! This program will help you find top-rated movies that fit your preferences.")


movies = pd.read_csv('cache/movies.csv', header=0, sep=',')

#filter df by user choices
#by year
min = int(movies['release_year'].dropna().min())
max = int(movies['release_year'].dropna().max())
min_year = st.slider("Year Range - Start", min_value=min, max_value=max)
max_year = st.slider("Year Range - End", min_value=min_year, max_value=max, value=max)
filtered = movies[(movies['release_year'] <= max_year) & (movies['release_year'] >= min_year)]

#by genre
genres = ['*ANY*']
for value in filtered['genre'].dropna():
    genres_per_movie = value.split(',')
    genres_per_movie = [genre.strip() for genre in genres_per_movie]
    for genre in genres_per_movie:
        if genre not in genres:
            genres.append(genre)
genres = sorted(genres)
genre = st.selectbox("Genre", genres)
if genre != '*ANY*':
    filtered = filtered[filtered['genre'].str.contains(genre, case=False, na=False)]

#by rating
ratings = ['*ANY*']
for value in filtered['rating'].dropna():
    if value not in ratings:
        ratings.append(value)
rating = st.selectbox("Rating", ratings)
if rating != '*ANY*':
    filtered = filtered[filtered['rating'] == rating]

#by runtime
min = int(movies['runtime_in_minutes'].dropna().min())
max = int(movies['runtime_in_minutes'].dropna().max())
min_runtime = st.slider("Length of Movie - Min", min_value=min, max_value=max)
max_runtime = st.slider("Length of Movie - Max", min_value=min_runtime, max_value=max, value=max)
filtered = filtered[(filtered['runtime_in_minutes'] <= max_runtime) & (filtered['runtime_in_minutes'] >= min_runtime)]

#filter by only high rated movies
if filtered.empty:
    st.write("No movies found with the selected criteria. Please try again.")
else:
    suggestions = filtered[filtered['tomatometer_status'] == "Certified Fresh"]
    if suggestions.empty:
        suggestions = filtered[filtered['tomatometer_status'] == "Fresh"]
        if suggestions.empty:
            suggestions = filtered[filtered['tomatometer_status'] == "Rotten"]
    if len(suggestions) > 3:
        suggestions = suggestions.sample(3)
    st.header("We recommend:")
    for index, row in suggestions.iterrows():
        st.subheader(row['movie_title'])
        st.write(f"Directed by {row['directors']}")
        st.write(f"{int(row['release_year'])} - {int(row['runtime_in_minutes'])} minutes - {row['tomatometer_rating']}% on Rotten Tomatoes")
        st.write(row['movie_info'])
        st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.header("See how movies that meet your preferences tend to rate:")
        fig = px.scatter(filtered, x="audience_rating", y="tomatometer_rating", color="tomatometer_status", hover_name="movie_title", hover_data='release_year')
        st.plotly_chart(fig)
    with col2:
        st.header("See how different factors correlate with ratings:")
        factor = st.selectbox("By", ['release_year', 'runtime_in_minutes', 'rating'])
        movies_agg = pd.pivot_table(movies, values="tomatometer_rating", index=factor, aggfunc="mean").reset_index()
        fig2 = px.bar(movies_agg, x=factor, y="tomatometer_rating", color="tomatometer_rating")
        st.plotly_chart(fig2)