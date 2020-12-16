import numpy as np
from tabulate import tabulate
from pydantic import validate_arguments, ValidationError

from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

from koalas.api import format_input


class AxisOption(str, Enum):
    row = "row"
    col = "col"
    dual = "dual"


class DataFrame:
    @validate_arguments
    def __init__(self, data: list, axis: AxisOption = AxisOption.col):
        self.data, self.headers = format_input(data, axis)

    def _to_string(self):
        return tabulate(self.data, headers=self.headers)

    def __repr__(self):
        return self._to_string()

    def __str__(self):
        return self._to_string()
