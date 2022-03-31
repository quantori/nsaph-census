"""
Generic code for running QC on a csv file.
Requires input csv file, qc yaml file, and qc log name
"""

from nsaph_utils.utils.context import Cardinality, Context, Argument
from nsaph_utils.qc.tester import Tester
import pandas as pd
import logging


class QCContext(Context):
    """
    Context object for performing QC on a generic CSV file, provided a path and a path to a QC Yaml
    file.
    """

    _csv_file = Argument("csv_file",
                         help="Path to csv file containing the data frame to be checked",
                         cardinality=Cardinality.single)

    _qc_file = Argument("qc_file",
                         help="Path to YAML file containing the tests to be run on CSV file in NSAPH format",
                         cardinality=Cardinality.single)
    _qc_log = Argument("qc_log",
                        help="Name of log file to log the results of the QC on",
                        cardinality=Cardinality.single)
    _log = Argument("log",
                    help="Optional path to primary log file used, If not provided, not used",
                    cardinality=Cardinality.single,
                    default=None,
                    required=False)
    _name = Argument("name",
                     help="Name to use with the test suite (optional)",
                     cardinality=Cardinality.single,
                     default=None,
                     required=False)

    def __init__(self):
        self.csv_file = None
        self.qc_file = None
        self.qc_log = None
        self.log = None
        self.name = None
        super().__init__(QCContext)


def initialize_logging(qc_log: str, log: str = None):

    if log:
        handler = logging.FileHandler(log, mode="a")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger = logging.getLogger("")
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    qc_handler = logging.FileHandler(qc_log, mode="w")
    qc_formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s - %(asctime)s')
    qc_handler.setFormatter(qc_formatter)

    qc_logger = logging.getLogger("nsaph_utils.qc")
    qc_logger.addHandler(qc_handler)
    qc_logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    context = QCContext().instantiate()
    initialize_logging(context.qc_log, context.log)

    if not context.name:
        name = context.csv_file
    else:
        name = context.name

    data = pd.read_csv(context.csv_file)
    test_suite = Tester(name, context.qc_file)

    test_suite.check(data)


