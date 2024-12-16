import pandas as pd
import numpy as np
import streamlit as st
import funcs as f

movies = pd.read_csv('data/rotten_tomatoes_movies.csv', header=0, sep=',')
#if no in_theaters_date, replace with N/A
movies['in_theaters_date'] = movies['in_theaters_date'].fillna('N/A')
#add year column to movies dataframe
movies['release_year'] = movies.apply(lambda row: f.get_year(row['in_theaters_date']), axis=1)
movies['runtime_in_minutes'] = movies.apply(lambda row: f.remove_outliers(row['runtime_in_minutes']), axis=1)
movies['rating'] = movies.apply(lambda row: f.clean_ratings(row['rating']), axis=1)
movies.to_csv('cache/movies.csv', index=False)