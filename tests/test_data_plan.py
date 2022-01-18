
#  Copyright (c) 2022. Harvard University
#
#  Developed by Harvard T.H. Chan School of Public Health
#  (HSPH) and Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Ben Sabath (https://github.com/mbsabath)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import os
import unittest

import census

DIR_STEM = os.path.dirname(__file__)


class DataPlanTest(unittest.TestCase):
    def test_load_yaml(self):
        plan = census.DataPlan(DIR_STEM + "/data_cache/test_vars.yml",
         geometry= "state", years=[x for x in range(2009, 2010)])
        self.assertEqual(list(plan.plan.keys()), [2009])
        self.assertEqual(len(plan.plan[2009]), 3)

    def test_assembly_run(self):
        plan = census.DataPlan(DIR_STEM + "/data_cache/test_vars.yml",
         geometry="state", years=[x for x in range(2009, 2010)])
        plan.assemble_data()
        self.assertTrue("poverty" in plan.data.columns)


if __name__ == '__main__':
    unittest.main()
