import numpy as np
from tabulate import tabulate
from pydantic import validate_arguments, ValidationError

from koalas.models import Axis
from koalas.api import format_input


class DataFrame:
    @validate_arguments
    def __init__(self, data: list, axis: Axis = Axis.col):
        self.data, self.headers = format_input(data, axis)

    def _to_string(self):
        return tabulate(self.data, headers=self.headers)

    def __repr__(self):
        return self._to_string()

    def __str__(self):
        return self._to_string()
