from collections import defaultdict
import numpy as np
from pnguin.models import Axis


def _format_to_cols(data):
    n_data = defaultdict(list)

    for datapoint in data:
        for key, value in datapoint.items():
            n_data[key].append(value)

    return dict(n_data)


def _format_to_rows(dl):
    return [dict(zip(dl, t)) for t in zip(*dl.values())]


def _transform_rows(x, t):
    if t == Axis.row:
        return x
    else:
        return _format_to_cols(x)


def _transform_cols(x, t):
    if t == Axis.col:
        return x
    else:
        return _format_to_rows(x)


def format_input(data, t):
    def _fmt(x):
        return Axis.row if isinstance(data, list) else Axis.col

    f = _transform_rows if _fmt(data) == Axis.row else _transform_cols
    return f(data, t)


def drop_nan_rows(rows, exclude):
    def _pull_target_elements(r, ex):
        if len(ex) == 0:
            return r.values()
        x = []
        for key, value in r.items():
            if key not in ex:
                x.append(value)
        return x

    n_rows = []
    for row in rows:
        targets = _pull_target_elements(row, exclude)
        if not np.isnan(targets):
            n_rows.append(row)
    return n_rows


def apply_rows(rows, f):
    return rows


def apply_cols(cols, f):
    return cols


def bq_to_rows(rows):
    def _reformat(x):
        pairs = x.items()
        row = {}
        for pair in pairs:
            key, value = pair
            row[key] = value
        return row

    return [_reformat(x) for x in rows]


def is_valid_index(idx, axis):
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
    if isinstance(k, slice):
        return [x[ii] for ii in range(*k.indices(len(x)))]
    elif isinstance(k, int):
        return [x[k]]
    else:
        return x[k]


def set_item(x, k, val):
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
