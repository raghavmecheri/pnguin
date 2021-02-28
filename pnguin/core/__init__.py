"""Some core functionality that depends on tying a few helper methods together with constructors
"""
from pydantic import validate_arguments, ValidationError

from pnguin.core.dataframe import DataFrame
from pnguin.core.remoteframes import SQLFrame, BQFrame
from pnguin.core.filter import Filter

from pnguin.api.io import read_csv_to_data
from pnguin.models import Axis


@validate_arguments
def read_csv(
    path: str, axis: Axis = Axis.col, delimiter: str = ",", headers: list = []
):
    """Given a valid path, read a csv file to a pnguin DataFrame

    Read a csv at a given path, and load the data into a pnguin DataFrame, with a given axis.

    Args:
            path (str): Path to csv file
            axis (Axis): Enum signifying what the dominant axis of the DataFrame must be
            delimiter (str): Delimiter to split row data (',' for csv files, and '\t' for csv files)
            headers (list): A header row -- if not specified, the first row of the csv will be used as a header

    Returns:
            pnguin.DataFrame: A DataFrame containing the data from the csv file

    """
    return DataFrame(read_csv_to_data(path, delimiter, headers), axis=axis)
