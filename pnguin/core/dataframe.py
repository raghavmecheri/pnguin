import numpy as np
from tabulate import tabulate
from pydantic import validate_arguments, ValidationError
from typing import Callable

from pnguin.core.frame import Frame
from pnguin.models import Axis
from pnguin.api.utils import (
    format_input,
    drop_nan_rows,
    apply_rows,
    apply_cols,
    is_valid_index,
    fetch_item,
    set_item,
)
from pnguin.api.io import print_warning


class DataFrame(Frame):
    @validate_arguments
    def __init__(self, data, axis: Axis = Axis.col, warnings: bool = True):
        self.axis = axis
        self.data = format_input(data, axis)
        self.warnings = warnings

    @validate_arguments
    def head(self, n: int = 5):
        if self.axis == Axis.row:
            return DataFrame(self.data[0 : n + 1], self.axis)
        return DataFrame(format_input(self.data, Axis.col), self.axis)

    @validate_arguments
    def dropna(self, exclude: list = [], inplace: bool = False):
        target = self._data_as_rows()
        rectified = drop_nan_rows(target, exclude)

        if inplace:
            self.data = format_input(rectified, self.axis)

        return format_input(rectified, self.axis)

    @validate_arguments
    def apply(self, x: Callable, axis: Axis = Axis.row, inplace: bool = False):
        target = self._data_as_rows() if axis == Axis.row else self._data_as_cols()
        applied = apply_rows(target, x) if axis == Axis.row else apply_cols(target, x)
        if inplace:
            self.data = format_input(applied, self.axis)
        return format_input(applied, self.axis)

    @validate_arguments
    def to_csv(self):
        raise NotImplementedError(
            "The to_csv function of the DataFrame class is yet to be implemented"
        )

    @validate_arguments
    def to_db(self):
        raise NotImplementedError(
            "The to_db function of the DataFrame class is yet to be implemented"
        )

    def _data_as_rows(self):
        return self.data if self.axis == Axis.row else format_input(self.data, Axis.row)

    def _data_as_cols(self):
        return self.data if self.axis == Axis.col else format_input(self.data, Axis.col)

    def _to_string(self):
        return tabulate(self.head().data, headers="keys")

    def __repr__(self):
        return self._to_string()

    def __str__(self):
        return self._to_string()

    def __getitem__(self, key):
        is_valid, msg, target_axis = is_valid_index(key, self.axis)
        if not is_valid:
            print_warning(
                "{} Pnguin auto-handles this, but this could take a second for larger datasets".format(
                    msg
                ),
                self.warnings,
            )
            return format_input(self.data, target_axis)[key]
        return fetch_item(self.data, key)

    def __setitem__(self, key, value):
        is_valid, msg, target_axis = is_valid_index(key, self.axis)
        if not is_valid:
            print_warning(
                "{} Pnguin auto-handles this, but this could take a second for larger datasets".format(
                    msg
                ),
                self.warnings,
            )
            data = (
                self._data_as_cols()
                if target_axis == Axis.col
                else self._data_as_rows()
            )
            set_item(data, key, value)
            self.data = format_input(data, self.axis)
        else:
            set_item(self.data, key, value)
