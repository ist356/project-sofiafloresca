import code.funcs as f
import numpy as np



def test_should_pass():
    print("\nAlways True!")
    assert True

def test_get_year():
    tests = [
        ('2022-05-23', 2022),
        ('1999-12-08', 1999),
        ('1913-07-12', 1913),
        ('2002-10-31', 2002)
    ]

    for date, expected in tests:
        print(f"Testing: {date}")
        print(f"EXPECTED: {expected}")
        actual = f.get_year(date) 
        print(f"ACTUAL  : {actual}")
        assert actual == expected

def test_remove_outliers():
    tests = [
        (2000, np.nan),
        (201, 201),
        (12, 12),
        (202, np.nan)
    ]

    for runtime, expected in tests:
        print(f"Testing: {runtime}")
        print(f"EXPECTED: {expected}")
        actual = f.remove_outliers(runtime) 
        print(f"ACTUAL  : {actual}")
        if np.isnan(expected):
            assert np.isnan(actual)
        else:
            assert actual == expected

def test_clean_ratings():
    tests = [
        ('PG-13', "PG-13"),
        ('G', "G"),
        ('R)', "R"),
        ('PG-13)', "PG-13")
    ]

    for rating, expected in tests:
        print(f"Testing: {rating}")
        print(f"EXPECTED: {expected}")
        actual = f.clean_ratings(rating) 
        print(f"ACTUAL  : {actual}")
        assert actual.find(expected) >=0