import unittest
import get_census


class DataPlanTest(unittest.TestCase):
    def test_load_yaml(self):
        plan = get_census.DataPlan("data_cache/test_vars.yml", geometry= "state", years=[x for x in range(2009, 2012)])
        self.assertEqual(list(plan.plan.keys()), [2009, 2010, 2011])
        self.assertEqual(len(plan.plan[2009]), 3)



if __name__ == '__main__':
    unittest.main()
