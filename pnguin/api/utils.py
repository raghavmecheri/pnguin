from collections import defaultdict
import numpy as np


def _format_to_cols(data):
    n_data = defaultdict(list)

    for datapoint in data:
        for key, value in datapoint.items():
            n_data[key].append(value)

    return dict(n_data), list(data[0].keys())


def _format_to_rows(dl):
    return [
        {key: value[index] for key, value in dl.items()}
        for index in range(len(dl.values()[0]))
    ]


_ROWS = {"row": lambda x: x, "col": _format_to_cols}

_COLS = {"row": _format_to_rows, "col": lambda x: x}

FORMATTER = {"row": _ROWS, "col": _COLS}


def format_input(data, t):
    def _fmt(x):
        return "row" if isinstance(data, list) else "col"

    return FORMATTER[_fmt(data)][t](data)


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
