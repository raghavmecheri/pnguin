"""A collection of pnguin.api utility functions.

This module contains a collection of utility functions and helpers that are used throughout the pnguin project.
"""
import math
from collections import defaultdict
import numpy as np
from pnguin.models import Axis


def _format_to_cols(data):
    """Helper method to take data in LOD (list of dict) format, and covert it to DOL (dict of lists)

    Args:
        data (list): List of dicts to be converted

    Returns:
        dict: A dict of lists representing data in column form

    """
    n_data = defaultdict(list)

    for datapoint in data:
        for key, value in datapoint.items():
            n_data[key].append(value)

    return dict(n_data)


def _format_to_rows(dl):
    """Helper method to take data in DOL (dict of lists) format, and convert it to LOD (list of dict)

    Args:
        data (list): Dict of lists to be converted

    Returns:
        list: A list of dicts representing data in row form

    """
    return [dict(zip(dl, t)) for t in zip(*dl.values())]


def _transform_rows(x, t):
    """A quick wrapper that transforms data into a certain format if required :)

    Args:
        x (list): Data in LOD form
        t (Axis): An Axis enum

    Returns:
        (any): Data in either LOD or DOL form based on the value of t

    """
    if t == Axis.row:
        return x
    else:
        return _format_to_cols(x)


def _transform_cols(x, t):
    """A quick wrapper that transforms data into a certain format if required :)

    Args:
        x (list): Data in DOL form
        t (Axis): An Axis enum

    Returns:
        (any): Data in either LOD or DOL form based on the value of t

    """
    if t == Axis.col:
        return x
    else:
        return _format_to_rows(x)


def format_input(data, t):
    """Format data into a specified form

    A helper method that given a DataFrame's data (either in DOL or LOD), transforms it into the required form

    Args:
        data (any): Data in either LOD or DOL form
        t (Axis): The desired orientation for our data

    Returns:
        any: Data in the desired (eiher LOD or DOL) form

    """

    def _fmt(x):
        return Axis.row if isinstance(data, list) else Axis.col

    f = _transform_rows if _fmt(data) == Axis.row else _transform_cols
    return f(data, t)


def drop_nan_rows(rows, exclude):
    """Drop those rows which have a NaN value in any of their columns

    Iterate through all the rows in a given DataFrame, and drop those which contain NaN values

    Args:
        rows (list): A list of rows to iterate over
        exclude (list): A list of keys to excempt from the drop_nan criteria

    Returns
        list: The same DataFrame, but with the NaN rows dropped (in LOD format)

    """

    def _pull_target_elements(r, ex):
        if len(ex) == 0:
            return list(r.values())
        x = []
        for key, value in r.items():
            if key not in ex:
                x.append(value)
        return x

    def _arr_contains_nan(arr):
        check = False
        for x in arr:

            if not isinstance(x, str) and math.isnan(x):
                check = True
        return check

    n_rows = []
    for row in rows:
        targets = _pull_target_elements(row, exclude)
        if not _arr_contains_nan(targets):
            n_rows.append(row)
    return n_rows


def apply_rows(rows, f):
    """Given a function f, apply it to every row.

    Iterate through every row, and apply a function f(x), where x is a dictionary object

    Args:
        rows (list): Row-wise DataFrame data (in LOD format)
        f (callable): A function to be called on every row

    Returns:
        list: A list of modified rows post function call

    """
    return [f(row) for row in rows]


def apply_cols(cols, f):
    """Given a function f, apply it to every column.

    Iterate through every column, and apply a function f(x), where x is a list

    Args:
        cols (list): Column-wise DataFrame data (in DOL format)
        f (callable): A function to be called on every column

    Returns:
        list: A list of modified cols post function call

    """
    return cols


def bq_to_rows(rows):
    """Reformat BigQuery's output to regular pnguin LOD data

    Reformat BigQuery's output format so we can put it into a DataFrame

    Args:
        rows (dict): A nested list of key-value tuples that need to be converted into a list of dicts

    Returns:
        list: A list of dictionaries based on the input x

    """

    def _reformat(x):
        pairs = x.items()
        row = {}
        for pair in pairs:
            key, value = pair
            row[key] = value
        return row

    return [_reformat(x) for x in rows]


def is_valid_index(idx, axis):
    """Given a subscript and an axis, check if it's valid

    Different DataFrames have different compatible axes.
    Some are supported via conversion, and some are incompatible.
    Filter through the possible combinations, and throw the required errors or print the required warnings.

    Args:
        idx (any): The subscript being passed
        axis (Axis): An enum signifying the Axis of the DataFrame.

    Returns:
        bool: An indicator of index validity
        str: A message, if any should be printed
        Axis: The target_axis that the data would need to be in

    """
    if not (isinstance(idx, int) or isinstance(idx, str) or isinstance(idx, slice)):
        raise Exception(
            "Only string, slice, or integer indices are supported, depending on whether your DataFrame is in row or column mode!"
        )
    if axis == Axis.row:
        if isinstance(idx, int) or isinstance(idx, slice):
            return True, None, Axis.row
        else:
            return (
                False,
                "Please use an integer value or an integer slice to select row(s) when your pnguin DataFrame is in row mode!",
                Axis.col,
            )
    else:
        if isinstance(idx, str):
            return True, None, Axis.col
        else:
            return (
                False,
                "Please use a string value to signify a column name when your pnguin DataFrame is in column mode!",
                Axis.row,
            )


def fetch_item(x, k):
    """Fetch an item from a given subscript

    Given a subscript, which may be a slice, a string, or an index, fetch the required items.
    This function assumes that the data-subscript pairs have already been checked using is_valid_index.

    Args:
        x (any): Data either in LOD or DOL form
        k (any): A subscript that may be a slice, an int, or a string

    Returns:
        any: Either a list of dicts, or a dict of lists according to what's being accessed

    """
    if isinstance(k, slice):
        return [x[ii] for ii in range(*k.indices(len(x)))]
    elif isinstance(k, int):
        return [x[k]]
    else:
        return x[k]


def set_item(x, k, val):
    """Helper method to set an item at index k to a given value val

    Based on the instance of the subscript and the instance of x, set the value val.

    Args:
        x (any): Data either in LOD or DOL form
        k (any): A subscript that may be a slice, an int, or a string
        val (any): The data to be set. May be either a single value, a list, or a list of dicts.

    Returns:
        any: Modified data either in DOL or LOD form

    """
    if isinstance(k, slice):
        if not isinstance(val, list):
            raise Exception(
                "Input format error: The value being set to a slice(d) index MUST be a list"
            )
        if not len(range(*k.indices(len(x)))) == len(val):
            raise Exception(
                "Input format error: The lengths of the target splice and the list being set must be equal"
            )
        for i in range(*k.indices(len(x))):
            x[i] = val[i]
    elif isinstance(k, int):
        if not (isinstance(val, dict)):
            raise Exception(
                "Input format error: The value being set to a row index MUST be a dict"
            )
        x[k] = val
    else:
        if not isinstance(val, list):
            raise Exception(
                "Input format error: The value being set to a column index MUST be a list"
            )
        if not len(x[k]) == len(val):
            raise Exception(
                "Input format error: The lengths of the target column and the column being set must be equal"
            )
        x[k] = val


def write_to_csv(df, filename):
    """Given a pnguin dataframe, write the data to a csv file

    Args:
        df (pnguin.DataFrame): DataFrame to write to csv
        filename (str): Filepath to write to

    """

    import csv

    def _col_to_csv(x, filename):
        with open(filename, "w") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(x.keys())
            writer.writerows(zip(*x.values()))

    def _row_to_csv(x, filename):
        keys = x[0].keys()
        with open(filename, "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(x)

    if df.axis == Axis.col:
        print("Writing your column-wise dataframe as a csv file at {}".format(filename))
        _col_to_csv(df.data, filename)
    else:
        print("Writing your row-wise dataframe as a csv file at {}".format(filename))
        _row_to_csv(df.data, filename)
