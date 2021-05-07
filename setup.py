from setuptools import setup, find_packages
from get_census import __version__

setup(
    name='get_census',
    version=__version__,
    packages=find_packages(),
    url='',
    license='',
    author='Ben Sabath',
    author_email='sabath@fas.harvard.edu',
    description='',
    entry_points="""
    [console_scripts]
    get_census=get_census:cli.census_cli
    """,
    include_package_data=True
)
