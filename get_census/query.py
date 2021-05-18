from .census_info import *
from .exceptions import *
import requests as r
import os
import pandas as pd
import logging


# Code for downloading the census data

SUPPORTED_GEOMETRIES = ["county", "state", "zcta", "block group", "tract"]

LOG = logging.getLogger(__name__)


def get_census_data(year: int, variables: list, geography: str, dataset: str, sum_file: str = None, key: str = None,
                    state: str = None, county: str = None):
    """

    :param year: Year of data that we are querying
    :param variables: list of strings containing the census variable names to request
    :param geography: Geographic resolution we're querying at (zcta, county, state)
    :param dataset: The census data set you want (dec, acs1, acs5, pums)
    :param sum_file: For the 2000 census, sf1 or sf3
    :param key: Your census API key. We recommend not passing it here and instead either setting
           the "GET_CENSUS_API_KEY" environmental variable or using the `set_api_key` function.
    :param state: 2 digit FIPS code of the state you want to limit the query to (i.e. "06" for CA)
    :param county: 3 digit FIPS code of the county you want to include. Requires state to be specified
    :return: a pandas DataFrame
    """

    if dataset == "acs":
        dataset = "acs5"

    if dataset == "census":
        dataset = "dec"

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
    if state is not None:
        options['in'] = 'state:' + state
        if county is not None:
            options['in'] += '+county:' + county
    if key is not None:
        options['key'] = os.environ['GET_CENSUS_API_KEY']

    num_tries = 0
    while num_tries < 5:
        try:
            out = r.get(endpoint, params=options)
            out.raise_for_status()
            break
        except:
            LOG.warning("Query Failed, re-trying")
            num_tries += 1
    if num_tries >= 5:
        LOG.critical("Unable to complete query after " + str(num_tries) + " tries")
        raise GetCensusException("Unable to complete query after " + str(num_tries) + " tries")

    out = out.json()
    out = pd.DataFrame(out[1:], columns=out[0])

    # handle conversion of variables to numeric
    for var in variables:
        try:
            out[var] = out[var].apply(pd.to_numeric)
        except ValueError:
            LOG.error("Unable to convert variable " + var + " to Numeric array")

    out['year'] = year

    return out


def clean_acs_vars(variables: list):
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


def prep_vars(variables: list):
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


def api_geography(geo: str):
    """
    go from function shorthand to the input the census api needs

    :param geo: shorthand for a given geography type
    :return: corrected geography name
    """
    geo = geo.lower()

    if geo not in SUPPORTED_GEOMETRIES:
        raise GetCensusException("Input Geometry not supported")

    if geo == "zcta":
        return "zip code tabulation area"
    else:
        return geo


def choose_sum_file(variables: list):
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
