import get_census
import pickle
import logging
from nsaph_utils.utils.context import Context, Argument, Cardinality


class AssembleContext(Context):

    _var_file = Argument("var_file",
                         help="Path to yaml file specifying census variables",
                         aliases=["vars"],
                         cardinality=Cardinality.single,
                         )
    _geometry = Argument("geometry",
                         help="Geographic Resolution to download census data at",
                         aliases=["geom"],
                         cardinality=Cardinality.single,
                         valid_values=get_census.query.SUPPORTED_GEOMETRIES
                         )
    _years = Argument("years",
                      aliases=["y"],
                      help="""
                      Year or list of years to download. For example, 
                      the following argument: 
                      `-y 1992:1995 1998 1999 2011 2015:2017` will produce 
                      the following list: 
                      [1992,1993,1994,1995,1998,1999,2011,2015,2016,2017]

                      Note that in the cwl_census module CLI, only the minimum and maximum year passed are used
                      and are passed to cwl_census.census_years() to ensure that only years that are available are used.
                      Additional variable level year control is determined by the variable specification yaml file. 
                      """,
                      cardinality=Cardinality.multiple,
                      default="2000:2019"
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
                       required=False
                       )
    _log = Argument("log",
                    help="Path to log file",
                    cardinality=Cardinality.single,
                    default="cwl_census.log")
    _pkl_file = Argument("pkl_file",
                         help="Path to temporary pkl file",
                         cardinality=Cardinality.single,
                         default="census.pkl")

    def __init__(self, doc=None):
        self.var_file = None
        self.geometry = None
        self.state = None
        self.county = None
        self.log = None
        self.pkl_file = None
        super().__init__(AssembleContext, doc)


def initialize_logging(log: str):
    handler = logging.FileHandler(log, mode="w")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return True


if __name__ == "__main__":
    context = AssembleContext().instantiate()
    initialize_logging(context.log)
    census = get_census.DataPlan(context.var_file,
                                 context.geometry,
                                 years=get_census.census_years(min(context.years), max(context.years)),
                                 state=context.state,
                                 county=context.county)
    census.assemble_data()

    with open(context.pkl_file, 'wb') as f:
        pickle.dump(census, f)
