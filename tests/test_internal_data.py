import unittest
import get_census.data

class TestDataDunctions(unittest.TestCase):

    def test_counties_data(self):
        counties = get_census.data.load_county_codes()
        self.assertEqual(len(counties.index), 3220)
        self.assertEqual(counties.columns.values.tolist(), ['NAME', 'state', 'county'])

    def test_state_data(self):
        states = get_census.data.load_state_codes()
        self.assertEqual(len(states.index), 52)
        self.assertEqual(states.columns.values.tolist(), ['NAME','state'])

if __name__ == '__main__':
    unittest.main()
