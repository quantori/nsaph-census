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

from setuptools import setup, find_packages

setup(
    name='census',
    version="0.3",
    url='https://github.com/NSAPH-Data-Platform/nsaph-census',
    license='',
    package_dir={
        "census": "./src/python/census"
    },
    packages=["census", "census.data"],
    author='Ben Sabath',
    author_email='sabath@fas.harvard.edu',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Harvard University :: Development",
        "Operating System :: OS Independent",
    ],
    description='',
    entry_points="""
    [console_scripts]
    census=census:cli.census_cli
    """,
    include_package_data=True,
    install_requires=[
        'certifi==2020.12.5',
        'chardet==4.0.0',
        'idna==2.10',
        'numpy==1.19.4',
        'pandas==1.1.5',
        'python-dateutil==2.8.1',
        'pytz==2020.5',
        'requests==2.25.1',
        'six==1.15.0',
        'urllib3==1.26.2',
    ],
    package_data={
        '': ["**/*.yaml"]
    },
)
