import requests as r
import os
from .exceptions import *

# Code for handling census metadata


def get_endpoint(year: int, dataset: str, sum_file: str = None):
    """
    Returns a string containing the URL to the census API endpoint

    :param year: The year for which you want data
    :param dataset: The census data set you want (dec, acs1, acs5, pums)
    :param sum_file: For the 2000 census, sf1 or sf3
    :return:
    """
    # Questions about where best to fail?
    # Do we throw an error here (or elsewhere while prepping the query

    if dataset not in ['dec', 'acs1', 'acs5']:
        raise GetCensusException("Input dataset not currently supported")

    out = "https://api.census.gov/data/" + str(year) + "/"

    if dataset == 'dec':
        if year not in [2000, 2010]:
            raise GetCensusException("Invalid year for decennial census")
        out += "dec/"
        if year == 2000:
            if sum_file not in ["sf1", "sf3"]:
                raise GetCensusException("Invalid summary file input")
            out += sum_file
        else:
            out += "sf1"
    elif dataset in ['acs1', 'acs5']:
        if year <= 2008:
            raise GetCensusException("Invalid year for ACS5")
        out += "acs/" + dataset
    #elif dataset == 'pums':
    #    assert year > 2008
    #    out += 'acs/acs5/pums'

    return out


def get_varlist(year: int, dataset: str, sum_file: str = None):
    """
    :param year: Year of data
    :param dataset: The census data set you want (dec, acs1, acs5, pums)
    :param sum_file: For the 2000 census, sf1 or sf3
    :return: Dataframe of available variables in a given data set
    """

    endpoint = get_endpoint(year, dataset, sum_file)

    out = r.get(endpoint + "/variables.json").json()

    varnames = list(out['variables'].keys())[3:]

    return varnames


def set_api_key(key: str):
    """
    Sets an environment variable to contain your census API key. To avoid needing to run this
    every session you can also permanently set GET_CENSUS_API_KEY to your key in your environment.

    :param key: Your Census API key as a string
    :return: nothing
    """
    os.environ['GET_CENSUS_API_KEY'] = key


def census_years(min_year: int = 2000, max_year: int = 2019):
    """
    Constructs a list of years for which census data is available in the range provided. At this point assumes
    we want the decennial census and acs5. Future functionality might expand to allow this to vary.

    :param min_year: minimum year we want data for
    :param max_year: max year we want data for (inclusive)
    :return: list of all years in specified range for which data is available
    """

    out = []
    if min_year <= 2000:
        out.append(2000)

    out = out + list(range(max(min_year, 2009), min(max_year, 2019) + 1))
    return out
