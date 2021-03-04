from .census_info import census_years
from .query import get_census_data, clean_acs_vars
import pandas as pd
import yaml
import nsaph_utils


class DataPlan:
    """
    a class containing information on how to create a desired set of census data.

    Members:

    * ``geometry``: which census geography this plan is for
    * ``years``: The ``list`` of years that the data should be queried for
    * ``plan``: A ``dict`` with keys of years, storing lists of ``VariableDef`` objects defining the variables to be
      calculated for that year. Created from a yaml file. LINK TO YAML INSTRUCTIONS HERE
    * ``data``: A pandas data frame created based on the defined data plan. only exists after the
      ``DataPlan.assemble_data()`` method is called.


    """


    def __init__(self, yaml_path, geometry, years=census_years()):
        """
        initialize a DataPlan object from a get_census yaml document
        :param yaml_path: path to a yaml file
        :param geometry: which census geography this plan is for
        :param years: The list of years to query data from. The census_years() function can
            calculate which years in your timeframe of interest can be queried for the decennial and
            5 year acs data. Note that this may not apply for the ACS1 or other data. That function may be
            updated in the future, but for now creating lists of years besides the defaults is left as an exercise
            for the interested reader.


        """
        self.geometry = geometry
        self.years = years
        if type(self.years) is int:
            self.years = [self.years]

        self.plan = dict()
        self.yaml_to_dict(yaml_path)
        self.__has_missing = False

        self.data = pd.DataFrame()

    def yaml_to_dict(self, yaml_path):
        """
        Convert a yaml file detailing how to get census variables in to a dictionary. Handles
        the issue of forward counting years to make future code readable.

        INSERT LINK TO CENSUS README TO GUIDE HOW TO WRITE THE YAML

        :param yaml_path:
        :return: dictionary


        """

        # Read in Raw YAML

        with open(yaml_path) as f:
            yaml_dict = yaml.load(f, Loader=yaml.FullLoader)

        for year in self.years:
            self.plan[year] = list()
            for varname in yaml_dict.keys():
                plan_year = find_year(year, list(yaml_dict[varname].keys()))
                if yaml_dict[varname][plan_year] != "skip":
                    self.plan[year].append(VariableDef(varname, yaml_dict[varname][plan_year]))

    def assemble_data(self):
        """
        Create a data frame for each geoid , for each year, with each variable as defined in the data plan

        :return: Assembled data frame stored in self.data
        """

        self.data = None  # Clear in case this has been run previously

        for year in self.years:
            year_data = None
            if len(self.plan[year]) == 0:
                continue

            for var_def in self.plan[year]:
                print(year, var_def.name)
                var_data = var_def.calculate_var(year, self.geometry)
                join_vars = list(set(var_data.columns).difference([var_def.name]))

                if year_data is None:
                    year_data = pd.DataFrame(columns=join_vars)

                year_data = pd.merge(year_data, var_data, how="outer", on=join_vars)

            if self.data is None:
                self.data = year_data
            else:
                self.data = self.data.append(year_data, ignore_index=True)

    def get_var_names(self):
        """
        Return a list containing all the variable names that are created in the data plan

        :return: List of strings
        """

        out = []
        for year in self.plan.keys():
            for var_def in self.plan[year]:
                out = list(set().union(out, [var_def.name]))

        return out

    def add_geoid(self):
        """
        add a single column named 'geoid' to self.data combining all portions of a data sets geographical identifiers

        :return: None
        """
        # handle known cases, then try a naive method

        if self.geometry == "county":
            self.data['geoid'] = self.data['state'] + self.data['county']
            return
        else:
            geo_vars = list(set(self.data.columns).difference(self.get_var_names() + ['year']))

            # assume that all geo_vars are string columns (should be the case with census data)
            self.data['geoid'] = ""
            for geo_var in geo_vars:
                self.data['geoid'] = self.data['geoid'] + self.data[geo_var]

    def create_missingness(self):
        """
        Create a row for all combinations of geospatial ID and year
        :return:
        """
        if self.__has_missing:
            print("Missing values already created.")
            return

        if "geoid" not in self.data.columns:
            self.add_geoid()

        all_vals = pd.DataFrame([[x, y] for x in range(min(self.data.year), max(self.data.year) + 1)
                                 for y in self.data.geoid.unique()], columns=['year', 'geoid'])
        self.data = pd.merge(all_vals, self.data, how="left", on=['year', 'geoid'])
        self.__has_missing = True

    def write_data(self, path, file_type = "csv"):
        """
        Write data  out to a file. Default method is to write out to csv. new methods can be implemented in the future.

        :param path: Path to write the data to
        :param file_type: Method to output data, currently only implemented for csv files
        :return: None, writes data to disk.
        """

        if file_type == "csv":
            self.data.to_csv(path)
            return
        else:
            print("No Method currently implemented for that file type")
            return

    def interpolate(self, method="ma"):
        """
        Fill in values
        :param method:
        :return:
        """
        assert method in nsaph_utils.interpolation.IMPLEMENTED_METHODS

        if not self.__has_missing:
            self.create_missingness()

        nsaph_utils.interpolate(self.data, self.get_var_names(), method, "year", "geoid")


class VariableDef:
    """
    Structured way of representing what we need to know for a variable.
    Members:
    * ``dataset``: a string. The data set used to calculate a variable, should be dec, acs1, acs5, or pums
    * ``num``: a list, the names of variables that make up the numerator
    * ``den``: a list, the names of the variables that make up the denominator. Can be missing
    * ``has_den``: a boolean, indicates whether or not there is a denominator.


    """

    def __init__(self, name: str, var_dict: dict):

        self.name = name
        self.dataset = list(var_dict.keys())[0]
        self.num = var_dict[self.dataset]['num']
        if type(self.num) is str:
            self.num = [self.num]

        if 'den' in var_dict[self.dataset].keys():
            self.has_den = True
            self.den = var_dict[self.dataset]['den']
            if type(self.den) is str:
                self.den = [self.den]
        else:
            self.has_den = False
            self.den = []

        if "acs" in self.dataset:
            self.make_acs_vars()

    def make_acs_vars(self):
        clean_acs_vars(self.num)
        if self.has_den:
            clean_acs_vars(self.den)

    def get_vars(self):
        """
        :return: a union of all census variables needed for this variable


        """
        return list(set().union(self.num, self.den))

    def do_query(self, year, geometry):
        """
        Run the query defined by the contained variables
        :param geometry: census geometry to query
        :param year: year of data to query
        :return: data frame of all census variables specified by the query


        """

        return get_census_data(year, self.get_vars(), geometry, self.dataset)

    def calculate_var(self, year, geometry):
        """
        Query the required data from the census, then calculate the variable defined
        :param year: year of data to query
        :param geometry: census geometry to query
        :return: a data frame with one column of the calcualted variable and the census geography columns


        """

        data = self.do_query(year, geometry)

        # calculate numerator
        data['num'] = 0
        for num_var in self.num:
            data['num'] += data[num_var]

        if self.has_den:
            data['den'] = 0
            for den_var in self.den:
                data['den'] += data[den_var]

        if self.has_den:
            data[self.name] = data['num'] / data['den']
        else:
            data[self.name] = data['num']

        data.drop(columns=self.get_vars(), inplace=True)
        data.drop(columns="num", inplace=True)
        if self.has_den:
            data.drop(columns="den", inplace=True)

        return data

    def __str__(self):
        out = ""
        out += "Name: " + self.name + "\n"
        out += "Dataset: " + self.dataset + "\n"
        out += "Num: " + str(self.num) + "\n"

        if self.has_den:
            out += "Den: " + str(self.den)

        return out

    def __repr__(self):
        out = "<"
        out += self.name + " "
        out += self.dataset + ">"

        return out


def find_year(year, year_list):
    """
    Internal helper function, not exported. Returns the first
    year in the list greater or equal to the year
    :param year: year of interest
    :param year_list:list: list of years, likely from a yaml census list
    :return: first year greater than or equal to "year" in "year_list"


    """

    year_list.sort()  # Should be sorted, but just in case
    for i in year_list:
        if i >= year:
            return i
