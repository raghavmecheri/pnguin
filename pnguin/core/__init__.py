from pydantic import validate_arguments, ValidationError

from pnguin.core.dataframe import DataFrame
from pnguin.core.remoteframes import SQLFrame, BQFrame

from pnguin.api.io import read_csv_to_data
from pnguin.models import Axis


@validate_arguments
def read_csv(
    path: str, axis: Axis = Axis.col, delimiter: str = ",", headers: list = []
):
    return DataFrame(read_csv_to_data(path, delimiter, headers), axis=axis)
