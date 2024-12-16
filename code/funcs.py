import pandas as pd
import numpy as np

def get_year(date: str):
    if date == 'N/A':
        year = np.nan
    else:
        year = int(date[0:4])
    return year

def remove_outliers(runtime: int):
    if runtime > 201:
        return np.nan
    else:
        return runtime

def clean_ratings(rating: str):
    if rating == 'PG-13)':
        return "PG-13"
    elif rating == 'R)':
        return "R"
    else:
        return rating