"""
utils.py
========================
Census utility functions
"""

import os

def show_api_keys():
    """
    Prints out api keys.
    """
    list_of_keys = ['CENSUS_API_KEY']

    for item in list_of_keys:
        if item not in os.environ.keys():
            print(f"Key: {item}, is not defined.")
        else:
            print(f"Key: {item}, Value: {os.environ[item]}")

        
