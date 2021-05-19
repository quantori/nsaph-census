import unittest
import get_census
import os
import pickle


class SchemaTestCase(unittest.TestCase):
    def test_schema_dict(self):
        with open( os.path.dirname(__file__) + "/data_cache/census_walkthrough_data.pkl", 'rb') as f:
            census_data = pickle.load(f)

        schema = census_data._schema_dict()
        self.assertEqual(list(schema.keys()), [census_data.geometry])
        self.assertEqual(list(schema[census_data.geometry].keys()), ["columns", "primary_key"])
        self.assertEqual(list(schema[census_data.geometry]["columns"].keys()),
                         ["geoid", "year"] + census_data.get_var_names())
        self.assertEqual(schema[census_data.geometry]["primary_key"], ["geoid", "year"])
        self.assertEqual(schema[census_data.geometry]["columns"]["year"]["type"], "INT")
        self.assertEqual(schema[census_data.geometry]["columns"]["geoid"]["type"], "VARCHAR(2)")
        self.assertEqual(schema[census_data.geometry]["columns"]["poverty"]["type"], "FLOAT4")


if __name__ == '__main__':
    unittest.main()
