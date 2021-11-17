
import unittest

import numpy as np

from census.exceptions import CensusException
from census.census_info import get_endpoint, get_varlist, census_years


class TestCensusInfo(unittest.TestCase):

    def test_endpoint_errors(self):
        with self.assertRaises(CensusException):
            get_endpoint(2009, "faskdf")
        with self.assertRaises(CensusException):
            get_endpoint(2013, "dec")
        with self.assertRaises(CensusException):
            get_endpoint(2000, "dec")
        with self.assertRaises(CensusException):
            get_endpoint(2007, "acs5")

    def test_endpoint(self):
        endpoint = get_endpoint(2017, "acs5")
        self.assertEqual(endpoint, "https://api.census.gov/data/2017/acs/acs5")
        endpoint = get_endpoint(2000, "dec", "sf3")
        self.assertEqual(endpoint, "https://api.census.gov/data/2000/dec/sf3")
        endpoint = get_endpoint(2010, "dec")
        self.assertEqual(endpoint, "https://api.census.gov/data/2010/dec/sf1")

    def test_get_varlist(self):
        varlist = get_varlist(2011, "acs5")
        self.assertIs(type(varlist), list)

    def test_census_years(self):
        cy = census_years(1985, 2013)
        self.assertEqual(cy, [2000, 2009, 2010, 2011, 2012, 2013])


if __name__ == '__main__':
    unittest.main()
