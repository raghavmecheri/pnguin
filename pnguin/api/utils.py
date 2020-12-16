from collections import defaultdict


def _format_to_col(data):
    n_data = defaultdict(list)

    for datapoint in data:
        for key, value in datapoint.items():
            n_data[key].append(value)

    return dict(n_data), list(data[0].keys())


def _format_to_rows(data):
    return data, list(data[0].keys())


def _format_to_dual(data):
    # FIXME - Todo
    return data, list(data[0].keys())


FORMATTER = {"row": _format_to_rows, "col": _format_to_col, "dual": _format_to_dual}


def format_input(data, t):
    return FORMATTER[t](data)


def pull_rows_from_cols(cols, s, n):
    rows = []
    for name, row in cols.items():
        for i in range(n):
            if i >= len(row):
                break
            if len(rows) > i:
                rows[i][name] = row[i]
            else:
                tmp = {}
                tmp[name] = row[i]
                rows.append(tmp.copy())
    return rows
