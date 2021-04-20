"""
Command Line Interface for the get_census python package
"""
from .query import SUPPORTED_GEOMETRIES
from .census_info import census_years
from .assemble_data import DataPlan
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
    _state = Argument("state",
                      help='2 digit FIPS code of the state you want to limit the query to (i.e. "06" for CA)',
                      cardinality=Cardinality.single,
                      default=None,
                      required=False
                      )
    _county = Argument("county",
                       help="3 digit FIPS code of the county you want to include. Requires state to be specified",
                       cardinality=Cardinality.single,
                       default=None,
                       required=False)
    _interpolate = Argument("interpolate",
                            help="""Years to interpolate for. Takes min year + max year formatted 
                            as <min_year>:<max_year>. Enter 'x' to skip interpolation""",
                            aliases=["i"],
                            cardinality=Cardinality.single,
                            default="1999:2019",
                            )
    _out_file = Argument("out_file",
                         aliases=["out"],
                         help="name of file to write output to",
                         cardinality=Cardinality.single,
                         default=None)
    _out_format = Argument("out_format",
                           help="file format to store output as.",
                           default="csv",
                           cardinality=Cardinality.single,
                           valid_values=DataPlan.supported_out_formats)

    def __init__(self, doc=None):
        self.var_file = None
        self.geometry = None
        self.state = None
        self.county = None
        self.interpolate = None
        self.out_file = None
        self.out_format = None
        super().__init__(CensusContext, doc)

    def validate(self, attr, value):
        value = super().validate(attr, value)

        if attr == "interpolate":
            if value == "x":
                return None
            else:
                value = value.split(":")
                out = dict()
                out["min"] = int(value[0])
                out["max"] = int(value[1])
                return out

        return value


def census_cli():
    context = CensusContext(__doc__).instantiate()
    census = DataPlan(context.var_file,
                      context.geometry,
                      years=census_years(min(context.years), max(context.years)),
                      state=context.state,
                      county=context.county)
    census.assemble_data()

    if context.interpolate:
        census.interpolate(min_year=context.interpolate["min"], max_year=context.interpolate["max"])

    census.write_data(context.out_file, file_type=context.out_format)
