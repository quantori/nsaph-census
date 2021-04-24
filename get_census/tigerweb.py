"""
Code for interacting with the Census TIGERWEb API
"""
import requests as r
import pandas as pd
from .query import prep_vars
from .data import load_state_codes
import os

GEOMETRY_CODES = {"zcta": 2,
                  "tract": 8,
                  "block group": 10,
                  "state": 84,
                  "county": 86}

TIGER_NAMES = {
    "zcta" : "ZCTA5",
    "tract": "TRACT",
    "county": "COUNTY",
    "state": "STATE",
    "block group": "BG"
}


class BBox:

    def __init__(self, xmin=-1.96724487545E7, ymin=-1678452.6019, xmax=1.62682738027E7, ymax=1.15436424852E7):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def __str__(self):
        return str(self.xmin) + "," + str(self.ymin) + "," + str(self.xmax) + "," + str(self.ymax)

    def subdivide(self, factor=2):
        """
        Create list of BBox objects that break up the axes of the parent obejct by `factor`. I.e. A factor of
        2 will create 4 child BBoc objects
        :param factor: Factor so subdivide by
        :return:
        """
        xdiff = (self.xmax - self.xmin)/factor
        ydiff = (self.ymax - self.ymin)/factor

        out = []

        for i in range(factor):
            for j in range(factor):
                out.append(BBox(xmin=self.xmin + (i * xdiff),
                                ymin=self.ymin + (j * ydiff),
                                xmax=self.xmin + ((i+1) * xdiff),
                                ymax=self.ymin + ((j+1) * ydiff)))

        return out


def tigerweb_endpoint(geometry):
    """
    Get the API endpoint for making
    :param geometry: type of census geometry to use
    :return: string of rest API URL endpoint
    """
    out = "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/tigerWMS_ACS2019/MapServer/"
    out += str(GEOMETRY_CODES[geometry])
    out += "/query"

    return out


def tigerweb_params(attributes=["GEOID"], split_factor: int=None):
    """
    Create a list of  dictionaries of the necessary parameters to query the census tigerweb API. Returns
    a list to enable combining of queries that return sets larger than the maximum number of objects

    :param attributes: List of names of attributes to include. You should always include "GEOID" to enable
      linking of features with other census data
    :param split_factor: Factor to divide the bounding box by to enable splitting up of large queries
    :return: list of dictionary of needed parameters
    """
    out = []
    bbox = BBox()

    if split_factor:
        boxes = bbox.subdivide(split_factor)
    else:
        boxes = [bbox]

    for box in boxes:
        params = dict()
        params["geometry"] = str(box)
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
        params["returnGeometry"] = "false"
        params["f"] = "pjson"

        out.append(params)

    return out


def get_area(geometry, sq_mi=True):
    """
    Create a data frame of Census GEOIDs and Area. Due to the Tigerweb API's limiting of
    the number of features per query to 100,000, block groups aren't currently supported through this wrapper.
    :param geometry: type of census geometry to use
    :param sq_mi:  Should areas be converted to square miles?
    :return: pandas data frame
    """

    url = tigerweb_endpoint(geometry)

    if geometry == "block group":
        split_factor = 10
    else:
        split_factor = None

    param_list = tigerweb_params(["GEOID", "AREALAND"], split_factor)
    out = None

    queries = 0
    for params in param_list:
        queries += 1
        print("Area query", queries, "of", len(param_list), end="           \r")
        result = r.get(url, params)
        result = list(map(lambda x: x['attributes'], result.json()['features']))
        result = pd.DataFrame(result)

        if out is None:
            out = result
        elif len(result.index) > 0:
            out = pd.merge(out, result, how="outer", on=["GEOID", "AREALAND"])
        elif len(result.index) == 100000:
            print("Max rows hit, increase split factor")
            return

    if sq_mi:
        out['AREALAND'] = out['AREALAND']/2589988  # 2589988 square meters to a square mile

    out.columns = out.columns.str.lower()
    return out


def tiger_line_url(geometry, year):
    """
    Return URL (or URLs) of zip file(s) containing shape files
    for a given census geography
    :param geometry: name of census geometry to download
    :param year: year of geometry to download
    :return: List of URLs
    """
    base = "https://www2.census.gov/geo/tiger/"

    if geometry == "zcta" and year == 2011:
        return tiger_line_url("zcta", 2010) # No ZCTAs listed in 2011 (for some reason)

    if year >= 2010:
        base += "TIGER" + str(year) + "/"
        base += TIGER_NAMES[geometry] + "/"
        if year == 2010:
            base += "2010/"
    else:
        year = 2000
        base += "TIGER2010/" + TIGER_NAMES[geometry] + "/2000/"

    out = []

    ## Define file stem for each geometry
    if geometry == "zcta":
        if year == 2000:
            base += "tl_2010_us_zcta500.zip"
        else:
            base += "tl_" + str(year) + "_us_zcta510.zip"
        out.append(base)
    elif geometry == "county":
        if year == 2000:
            base += "tl_2010_us_county00.zip"
        elif year == 2010:
            base += "tl_2010_us_county10.zip"
        else:
            base += "tl_" + str(year) + "_us_county.zip"
        out.append(base)
    elif geometry == "state":
        if year == 2000:
            base += "tl_2010_us_state00.zip"
        elif year == 2010:
            base += "tl_2010_us_state10.zip"
        else:
            base += "tl_" + str(year) + "_us_state.zip"
        out.append(base)
    elif geometry == "block group":
        if year == 2000:
            base += "tl_2010_"
            for state in load_state_codes()['state']:
                out.append(base + state + "_bg00.zip")
        elif year == 2010:
            base += "tl_2010_"
            for state in load_state_codes()['state']:
                out.append(base + state + "_bg10.zip")
        else:
            base += "tl_" + str(year) + "_"
            for state in load_state_codes()['state']:
                out.append(base + state + "_bg.zip")
    elif geometry == "tract":
        if year == 2000:
            base += "tl_2010_"
            for state in load_state_codes()['state']:
                out.append(base + state + "_tract00.zip")
        elif year == 2010:
            base += "tl_2010_"
            for state in load_state_codes()['state']:
                out.append(base + state + "_tract10.zip")
        else:
            base += "tl_" + str(year) + "_"
            for state in load_state_codes()['state']:
                out.append(base + state + "_tract.zip")
    else:
        print("invalid geography")
        return

    return out


def download_file(url, out_dir):
    local_filename =  out_dir + "/" + url.split('/')[-1]
    # NOTE the stream=True parameter below
    with r.get(url, stream=True) as result:
        result.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in result.iter_content(chunk_size=1024**2):
                f.write(chunk)
                print("#", end='')
        print()
    return local_filename


def download_geometry(geometry, year=2019, out_dir="."):
    """
    Get spatial information for a census geometry in geojson format and save it to disk
    :param geometry: type of census geometry to use
    :param out_dir: Directory to save downloaded files in. Note that due to requiring multiple
      downloads, tract and block group downloads will create a directory if no out_dir is defined.
    :return:
    """

    if geometry == "tract" and out_dir == ".":
        out_dir = "tract"
    elif geometry == "block group" and out_dir == ".":
        out_dir = "bg"

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    urls = tiger_line_url(geometry, year)

    for url in urls:
        download_file(url, out_dir)
