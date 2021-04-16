"""
Code for running the get_census functionality as a python cli
"""
from .query import SUPPORTED_GEOMETRIES
from nsaph_utils.utils.context import Context, Argument, Cardinality

class CensusContext(Context):
    """
    Context object supporting the CLI functionality of this package
    """
    _var_file = Argument("var_file",
                         help="Path to yaml file specifying census variables",
                         aliases=["vars"],
                         cardinality=Cardinality.single,
                         )
    _geometry = Argument("geometry",
                         help="Geographic Resolution to download census data at",
                         aliases=["geom"],
                         cardinality=Cardinality.single,
                         valid_values=SUPPORTED_GEOMETRIES
                         )



