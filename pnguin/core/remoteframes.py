import numpy as np
from tabulate import tabulate
from pydantic import validate_arguments, ValidationError
from typing import Any, Callable

from pnguin.core.frame import RemoteFrame
from pnguin.core.dataframe import DataFrame
from pnguin.models import Axis
from pnguin.api.utils import (
    format_input,
    drop_nan_rows,
    apply_rows,
    apply_cols,
    bq_to_rows,
)


class SQLFrame(RemoteFrame):
    @validate_arguments
    def __init__(self, connection: Any, table_name: str):
        self.connection = connection
        self.table_name = table_name

    @validate_arguments
    def head(self, n: int = 5):
        cursor = self.connection.cursor()
        sql = "SELECT * FROM `{}` LIMIT {}".format(self.table_name, n)
        cursor.execute(sql)
        result = cursor.fetchall()
        return DataFrame(result, Axis.row)

    def dropna(self, exclude: list = [], inplace: bool = False):
        return None

    def apply(self, x: Callable, axis: Axis = Axis.col, inplace: bool = False):
        return None

    def to_csv(self):
        return None

    def to_df(self):
        return None

    def _to_string(self):
        return self.head()

    def __repr__(self):
        return self._to_string()

    def __str__(self):
        return self._to_string()


class BQFrame(RemoteFrame):
    @validate_arguments
    def __init__(self, connection: Any, table_name: str):
        self.connection = connection
        self.table_name = table_name

    @validate_arguments
    def head(self, n: int = 5):
        sql = "SELECT * FROM `{}` LIMIT {}".format(self.table_name, n)
        query_job = self.connection.query(sql)
        result = query_job.result()
        return DataFrame(bq_to_rows(result), Axis.row)

    def _to_string(self):
        return self.head()

    def __repr__(self):
        return self._to_string()

    def __str__(self):
        return self._to_string()
