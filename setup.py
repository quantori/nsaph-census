from setuptools import setup
import setuptools
from get_census import __version__

setup(
    name='get_census',
    version=__version__,
    url='',
    license='',
    packages=setuptools.find_packages(exclude=['docs*', 'tests*']),
    author='Ben Sabath',
    author_email='sabath@fas.harvard.edu',
    description='',
    entry_points="""
    [console_scripts]
    get_census=get_census:cli.census_cli
    """,
    include_package_data=True
)
