
import os
import pandas as pd

DATA_DIR = os.path.dirname(__file__)


def load_county_codes():
    """
    Read in data file listing all counties in the US, with their state and county FIPS codes

    :return: pandas data frame
    """

    file_path = DATA_DIR + os.sep + "county_fips.csv"
    return pd.read_csv(file_path, dtype=str)


def load_state_codes():
    """
    Read in data file listing all states in the US, with their FIPS codes

    :return: pandas data frame
    """

    file_path = DATA_DIR + os.sep + "state_fips.csv"
    return pd.read_csv(file_path, dtype=str)