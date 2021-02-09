from .census_info import census_years
import pandas as pd
import yaml

class DataPlan:
    """
    a class de
    """
    def __init__(self, yaml_path, geometry, years=census_years()):
        """
        initialize a DataPlan object from a get_census yaml document
        :param yaml_path: path to a yaml file
        """
        self.geometry = geometry
        self.years = years
        self.plan = dict()
        self.yaml_to_dict(yaml_path, years)

        self.data = None


    def yaml_to_dict(self, yaml_path, years):
        """
        Convert a yaml file detailing how to get census variables in to a dictionary. Handles
        the issue of forward counting years to make future code readable.

        INSERT LINK TO CENSUS README TO GUIDE HOW TO WRITE THE YAML

        :param yaml_path:
        :return: dictionary
        """

        ## Read in Raw YAML

        with open(yaml_path) as f:
            yaml_dict = yaml.load(f, Loader=yaml.FullLoader)

        for year in years:
            self.plan[year] = list()
            for varname in yaml_dict.keys():
                plan_year = find_year(year, list(yaml_dict[varname].keys()))
                self.plan[year].append(VariableDef(varname, yaml_dict[varname][plan_year]))




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
        else:
            self.has_den = True
            self.den = den

    def __init__(self, name, var_dict):

        self.name = name
        self.dataset = list(var_dict.keys())[0]
        self.num = var_dict[self.dataset]['num']

        if 'den' in var_dict[self.dataset].keys():
            self.has_den = True
            self.den = var_dict[self.dataset]['den']
        else:
            self.has_den = False

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

    year_list.sort()  #Should be sorted, but just in case
    for i in year_list:
        if i >= year:
            return i