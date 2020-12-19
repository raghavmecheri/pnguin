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
