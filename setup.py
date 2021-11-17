from setuptools import setup, find_packages
from census import __version__

setup(
    name='census',
    version=__version__,
    url='',
    license='',
    packages=find_packages(exclude=['docs*', 'tests*']),
    author='Ben Sabath',
    author_email='sabath@fas.harvard.edu',
    description='',
    entry_points="""
    [console_scripts]
    census=census:cli.census_cli
    """,
    include_package_data=True
)
