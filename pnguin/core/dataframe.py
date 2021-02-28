import numpy as np
from tabulate import tabulate
from pydantic import validate_arguments, ValidationError
from typing import Callable

from pnguin.core.frame import Frame
from pnguin.core.filter import Filter
from pnguin.models import Axis
from pnguin.api.utils import (
    format_input,
    drop_nan_rows,
    apply_rows,
    apply_cols,
    is_valid_index,
    fetch_item,
    set_item,
    write_to_csv,
)
from pnguin.api.io import print_warning


class DataFrame(Frame):
    """Manipulate and access large tables of data in-memory

    A minimalist version of the Pandas DataFrame class, but with bi-axial support.
    Specify an axis to optimise the time complexity of your operations, but access elements via both row and column.
    pnguin will convert the format of your data on the fly to make it all work.

    Attributes:
        axis (str, optional): The primary axis of your DataFrame. Set to 'col' by default
        data (any): Your DataFrame's underlying data, formatted either as a list of dicts (rows) or a dict of lists (columns) based on your input axis
        warnings (bool, optional): A flag determining whether pnguin will print warnings. True by default

    """

    @validate_arguments
    def __init__(self, data, axis: Axis = Axis.col, warnings: bool = True):
        """Create a new pnguin DataFrame

        Args:
            data (any): Input data for the pnguin dataframe, either in list of dicts (rows) or dict of lists (columns) form
            axis (str, optional): The primary axis that the DataFrame is to operate using. 'col' by default
            warnings (bool, optional): A flag determining whether pnguin will print warnings. True by default

        Returns:
            (pnguin.DataFrame): A new pnguin DataFrame

        """
        self.axis = axis
        self.data = format_input(data, axis)
        self.warnings = warnings

    @validate_arguments
    def head(self, n: int = 5):
        """Return the head (or the top n rows) of your DataFrame

        Args:
            n (int, optional): The number of rows to be returned. 5 by default

        Returns:
            (pnguin.DataFrame): A new DataFrame with the first n rows of self

        """
        if self.axis == Axis.row:
            return DataFrame(self.data[0:n], self.axis)

        row_data = format_input(self.data, Axis.row)
        return DataFrame(row_data[0:n], self.axis)

    @validate_arguments
    def dropna(self, exclude: list = [], inplace: bool = False):
        """Drop those rows with NaN values

        Args:
            exclude (list, optional): Certain column names that may be excempt from the dropping criteria. [] by default
            inplace (bool, optional): Perform this operation in-place, and don't return a new DataFrame. False by default

        Returns:
            (pnguin.DataFrame or None)

        """
        target = self._data_as_rows()
        rectified = drop_nan_rows(target, exclude)

        if inplace:
            self.data = format_input(rectified, self.axis)
            return None

        return DataFrame(rectified, self.axis)

    @validate_arguments
    def apply(self, x: Callable, axis: Axis = Axis.row, inplace: bool = False):
        """Apply a given function per row or per column on a DataFrame

        Args:
            x (callable): A function to be run per row/column
            axis (str): The target axis to be operated on ('row' by default)
            inplace (bool): Determines whether the existing DataFrame will be modified, or a new DataFrame will be returned

        Returns:
            (pnguin.DataFrame or None)

        """
        target = self._data_as_rows() if axis == Axis.row else self._data_as_cols()
        applied = apply_rows(target, x) if axis == Axis.row else apply_cols(target, x)
        if inplace:
            self.data = format_input(applied, self.axis)
            return None
        return DataFrame(applied, self.axis)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def filter(self, f: Filter):
        data = self._data_as_rows()
        filtered = []
        for row in data:
            if f.does_conform(row):
                filtered.append(row)
        return DataFrame(filtered, self.axis)

    @validate_arguments
    def iterate(self):
        """Return a row-wise pnguin iterator

        Args:
            axis (str): The target axis to be iterated ('row' by default)

        Returns:
            Iterable object of rows/columns
        """
        return iter(self._data_as_rows())

    @validate_arguments
    def to_csv(self, filename: str):
        write_to_csv(self, filename)

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
