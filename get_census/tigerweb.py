"""
Code for interacting with the Census TIGERWEb API
"""
import requests as r
import pandas as pd
from .query import prep_vars

GEOMETRY_CODES = {"zcta": 2,
                  "tract": 8,
                  "state": 84,
                  "county": 86}

BBOX = "-1.96724487545E7,-1678452.6019,1.62682738027E7,1.15436424852E7"


def tigerweb_endpoint(geometry):
    """
    Get the API endpoint for making
    :param geometry: type of census geometry to use
    :return: string of rest API URL endpoint
    """
    out = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_Current/MapServer/"
    out += str(GEOMETRY_CODES[geometry])
    out += "/query"

    return out


def tigerweb_params(attributes=["GEOID"], geojson=False):
    """
    Create a dictionary of the necessary parameters to query the census tigerweb API
    :param attributes: List of names of attributes to include. You should always include "GEOID" to enable
      linking of features with other census data
    :param geojson: Should a geojson containing spatial information be returned
    :return: dictionary of needed parameters
    """
    params = dict()
    params["geometry"] = BBOX
    params["geometryType"] = "esriGeometryEnvelope"
    params["spatialRel"] = "esriSpatialRelIntersects"
    params["outFields"] = prep_vars(attributes)
    params["returnTrueCurves"] = "false"
    params["returnTrueCurves"] = "false"
    params["returnIdsOnly"] = "false"
    params["returnCountOnly"] = "false"
    params["returnZ"] = "false"
    params["returnM"] = "false"
    params["returnExtentsOnly"] = "false"

    if geojson:
        params["returnGeometry"] = "true"
        params["f"] = "geojson"
    else:
        params["returnGeometry"] = "false"
        params["f"] = "pjson"

    return params


def get_area(geometry, sq_mi=True):
    """
    Create a data frame of Census GEOIDs and Area. Due to the Tigerweb API's limiting of
    the number of features per query to 100,000, block groups aren't currently supported through this wrapper.
    :param geometry: type of census geometry to use
    :param sq_mi:  Should areas be converted to square miles?
    :return: pandas data frame
    """

    url = tigerweb_endpoint(geometry)
    params = tigerweb_params(["GEOID", "AREALAND"])

    out=r.get(url, params)
    out = list(map(lambda x: x['attributes'], out.json()['features']))
    out = pd.DataFrame(out)

    if sq_mi:
        out['AREALAND'] = out['AREALAND']/2589988  # 2589988 square meters to a square mile

    out.columns = out.columns.str.lower()
    return out


def get_geometry(geometry, out_name=None):
    """
    Get spatial information for a census geometry in geojson format and save it to disk
    :param geometry: type of census geometry to use
    :param out_name: filename to save as. Defaults to <geometry>_geometry.geojson
    :return:
    """

    if not out_name:
        out_name = geometry + "_geometry.json"

    url = tigerweb_endpoint(geometry)
    params = tigerweb_params(geojson=True)

    out = r.get(url, params).content

    with open(out_name, 'w') as f:
        f.write(out)
