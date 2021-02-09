from .census_info import *
import requests as r
import os
import pandas as pd


# Code for downloading the census data


def get_census_data(year, variables, geography, dataset, sum_file=None, key=None):
    """

    :param year: Year of data that we are querying
    :param variables: list of strings containing the variable names to request
    :param geography: Geographic resolution we're querying at
    :param dataset: The census data set you want (dec, acs1, acs5, pums)
    :param sum_file: For the 2000 census, sf1 or sf3
    :param key: Your census API key. We recommend not passing it here and instead either setting
           the "GET_CENSUS_API_KEY" environmental variable or using the `set_api_key` function.
    :return: a pandas DataFrame
    """

    if dataset == "acs": dataset = "acs5"
    if dataset == "census": dataset = "dec"

    if year == 2000 and dataset == "dec" and sum_file is None:
        sum_file = choose_sum_file(variables)

    endpoint = get_endpoint(year, dataset, sum_file)
    geography = api_geography(geography)

    if key is None:
        if "GET_CENSUS_API_KEY" in os.environ.keys():
            key = os.environ["GET_CENSUS_API_KEY"]

    if type(variables) is str:
        variables = [variables]

    if dataset in ["acs1", "acs5"]:
        clean_acs_vars(variables)

    options = dict()
    options['get'] = prep_vars(variables)
    options['for'] = geography
    if key is not None:
        options['key'] = os.environ['GET_CENSUS_API_KEY']

    out = r.get(endpoint, params=options).json()
    out = pd.DataFrame(out[1:], columns=out[0])
    out['year'] = year

    return out


def clean_acs_vars(variables):
    """
    Ensure that the estimate value is specified for a list of ACS variables
    :param variables: list of strings ccontaining the variable names to request
    :return: list of strings containing ACS vars, postpended with an "E"
         (where not previously postended)
    """

    # If vars is not a string, assume it is a list of strings
    for i in range(len(variables)):
        if variables[i][-1] != "E":
            variables[i] += "E"


def prep_vars(variables):
    """
    Convert from a list to a comma separated string
    :param variables: list of vars
    :return: comma separated string
    """

    # if vars is not a string, assume it's a list of multiple strings
    out = ""
    for i in range(len(variables) - 1):
        out += variables[i]
        out += ","

    out += variables[-1]

    return out


def api_geography(geo):
    """
    go from function shorthand to the input the census api needs
    :param geo: shorthand for a given geography type
    :return: corrected geography name
    """
    geo = geo.lower()

    assert geo in ["county", "state", "zcta"]

    if geo == "zcta":
        return "zip code tabulation area"
    else:
        return geo

def choose_sum_file(variables):
    """
    Internal function, not exported
    If we're querying the 2000 US census, and we're not sure which summary file to
    use, we need to check to see if the variables listed are available in sf1. If they
    are, we use sf1, if not we use sf3.
    """

    varlist = get_varlist(2000, "dec", "sf1")

    sf1 = True
    for var in variables:
        sf1 = sf1 and (var in varlist)

    if sf1:
        return "sf1"
    else:
        return "sf3"


