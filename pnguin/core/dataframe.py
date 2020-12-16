import numpy as np
from tabulate import tabulate
from pydantic import validate_arguments, ValidationError

from pnguin.models import Axis
from pnguin.api import format_input, pull_rows_from_cols


class DataFrame:
    @validate_arguments
    def __init__(self, data: list, axis: Axis = Axis.col):
        self.axis = axis
        self.data, self.headers = format_input(data, axis)

    def head(self, n=5):
        if self.axis == Axis.row:
            return DataFrame(self.data[0 : n + 1], self.axis)
        return DataFrame(pull_rows_from_cols(self.data, 0, n), self.axis)

    def _to_string(self):
        return tabulate(self.head().data, headers=self.headers)

    def __repr__(self):
        return self._to_string()

    def __str__(self):
        return self._to_string()
