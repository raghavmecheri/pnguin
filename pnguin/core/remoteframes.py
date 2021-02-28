import numpy as np
from tabulate import tabulate
from pydantic import validate_arguments, ValidationError
from typing import Any, Callable

from pnguin.core.frame import RemoteFrame, Frame
from pnguin.core.dataframe import DataFrame
from pnguin.models import Axis
from pnguin.api.utils import (
    format_input,
    drop_nan_rows,
    apply_rows,
    apply_cols,
    bq_to_rows,
)
from pnguin.api.io import print_warning


class SQLFrame(RemoteFrame):
    @validate_arguments
    def __init__(self, connection: Any, table_name: str, warnings=True):
        self.connection = connection
        self.table_name = table_name
        self.warnings = warnings
        self.query_list = []

    @validate_arguments
    def head(self, n: int = 5) -> Frame:
        data = self._get_data(n)
        return DataFrame(data, Axis.row)

    @validate_arguments
    def dropna(self, exclude: list = []) -> Frame:
        cursor = self.connection.cursor()

        def _interpolate(x):
            return "{} IS NOT NULL".format(x)

        sql = (
            "SELECT * FROM `{}` WHERE ".format(self.table_name)
            + " AND ".join([_interpolate(x) for x in self._fetch_cols(exclude)]).strip()
        )
        cursor.execute(sql)
        result = cursor.fetchall()
        return DataFrame(result, Axis.row)

    @validate_arguments
    def apply(self, x: Callable, axis: Axis = Axis.col) -> Frame:
        print_warning(
            "This function call currently just invokes the pnguin.core.DataFrame class' apply function, and needs a facelift. If you'd like to give us a hand, please check out: https://github.com/raghavmecheri/pnguin/issues/9",
            self.warnings,
        )
        data = self._get_data()
        df = DataFrame(data, axis)
        df = df.apply(x, axis)
        return df

    @validate_arguments
    def to_csv(self, filename: str) -> Frame:
        data = self._get_data()
        df = DataFrame(data, Axis.col)
        df.to_csv(filename)

    @validate_arguments
    def to_df(self, axis: Axis = Axis.col) -> Frame:
        data = self._get_data()
        return DataFrame(data, axis)

    def _to_string(self):
        return self.head()

    def __repr__(self):
        return self._to_string()

    def __str__(self):
        return self._to_string()

    def _get_data(self, limit: int = 0):
        cursor = self.connection.cursor()
        sql = (
            "SELECT * FROM `{}` LIMIT {}".format(self.table_name, limit)
            if limit > 0
            else "SELECT * FROM `{}`".format(self.table_name)
        )
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def _fetch_cols(self, exclude):
        cursor = self.connection.cursor()
        sql = "SHOW COLUMNS FROM `{}`".format(self.table_name)
        cursor.execute(sql)

        cols = []
        for col in cursor.fetchall():
            if col["Field"] not in exclude:
                cols.append(col["Field"])
        return cols


class BQFrame(RemoteFrame):
    @validate_arguments
    def __init__(self, connection: Any, table_name: str):
        self.connection = connection
        self.table_name = table_name
        self.query_list = []

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
