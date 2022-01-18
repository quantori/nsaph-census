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

import unittest
import census.data

class TestDataDunctions(unittest.TestCase):

    def test_counties_data(self):
        counties = census.data.load_county_codes()
        self.assertEqual(len(counties.index), 3220)
        self.assertEqual(counties.columns.values.tolist(), ['NAME', 'state', 'county'])

    def test_state_data(self):
        states = census.data.load_state_codes()
        self.assertEqual(len(states.index), 52)
        self.assertEqual(states.columns.values.tolist(), ['NAME','state'])

if __name__ == '__main__':
    unittest.main()
