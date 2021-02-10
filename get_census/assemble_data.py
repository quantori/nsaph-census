from .census_info import census_years
from .query import get_census_data, clean_acs_vars
import pandas as pd
import yaml

class DataPlan:
    """
    a class containing information on how to create a desired set of census data.
    Members:
        geometry: which census geography this plan is for
        years: The list of years that the data should be queried for
        plan: A dictionary with keys of years, storing lists of VariableDef objects defining the
            variables to be calculated for that year. Created from a yaml file. LINK TO YAML INSTRUCTIONS HERE
        data: A pandas data frame created based on the defined data plan. only exists after the DataPlan.assemble_data()
        method is called.
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
        if type(self.years) is int: self.years = [self.years]

        self.plan = dict()
        self.yaml_to_dict(yaml_path)

        self.data = None


    def yaml_to_dict(self, yaml_path):
        """
        Convert a yaml file detailing how to get census variables in to a dictionary. Handles
        the issue of forward counting years to make future code readable.

        INSERT LINK TO CENSUS README TO GUIDE HOW TO WRITE THE YAML

        :param yaml_path:
        :param years:
        :return: dictionary
        """

        ## Read in Raw YAML

        with open(yaml_path) as f:
            yaml_dict = yaml.load(f, Loader=yaml.FullLoader)

        for year in self.years:
            self.plan[year] = list()
            for varname in yaml_dict.keys():
                plan_year = find_year(year, list(yaml_dict[varname].keys()))
                self.plan[year].append(VariableDef(varname, yaml_dict[varname][plan_year]))

    def assemble_data(self):
        """
        Create a data frame for each geoid each year, for
        :return:
        """

        self.data = None # Clear in case this has been run previously

        for year in self.years:
            year_data = None
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



class VariableDef:
    """
    Structured way of representing what we need to know for a variable.
    Members:
        dataset: a string. The data set used to calculate a variable, should be dec, acs1, acs5, or pums
        num: a list, the names of variables that make up the numerator
        den: a list, the names of the variables that make up the denominator. Can be missing
        has_den: a boolean, indicates whether or not there is a denominator.
    """

    def __init__(self, name, dataset, num, den=None):

        self.name = name
        self.dataset = dataset
        self.num = num
        if den is None:
            self.has_den = False
            self.den = []
        else:
            self.has_den = True
            self.den = den

        if "acs" in self.dataset: self.make_acs_vars()


    def __init__(self, name, var_dict):

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

        if "acs" in self.dataset: self.make_acs_vars()

    def make_acs_vars(self):
        clean_acs_vars(self.num)
        if self.has_den: clean_acs_vars(self.den)

    def get_vars(self):
        """
        Return a union of all census variables needed for this variable
        """
        return list(set().union(self.num, self.den))

    def do_query(self, year, geometry):
        """
        query the US census
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

        ## calculate numerator
        data['num'] = 0
        for num_var in self.num:
            data['num'] += data[num_var]

        if self.has_den:
            data['den'] = 0
            for den_var in self.den:
                data['den'] += data[den_var]

        if self.has_den:
            data[self.name] = data['num']/data['den']
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