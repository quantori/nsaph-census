import unittest
import census
import os

DIR_STEM = os.path.dirname(__file__)


class DataPlanTest(unittest.TestCase):
    def test_load_yaml(self):
        plan = census.DataPlan(DIR_STEM + "/data_cache/test_vars.yml", geometry= "state", years=[x for x in range(2009, 2012)])
        self.assertEqual(list(plan.plan.keys()), [2009, 2010, 2011])
        self.assertEqual(len(plan.plan[2009]), 3)

    def test_assembly_run(self):
        plan = census.DataPlan(DIR_STEM + "/data_cache/test_vars.yml", geometry="state", years=[x for x in range(2010, 2012)])
        plan.assemble_data()
        self.assertTrue("poverty" in plan.data.columns)



if __name__ == '__main__':
    unittest.main()
