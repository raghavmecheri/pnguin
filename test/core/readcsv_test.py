import pytest
import json

import pnguin as pg


def _fetch_mock_payloads():
    with open("test/data/mockReadCsv.json") as f:
        return json.load(f)


@pytest.mark.parametrize("payload", [x for x in _fetch_mock_payloads()])
def test_read_csv_data(payload):
    path, length, axis, need_headers = (
        payload["path"],
        payload["length"],
        payload["axis"],
        payload["specifyHeaders"],
    )

    if not need_headers:
        df = pg.read_csv(path, axis=axis)
    else:
        df = pg.read_csv(
            path, axis=axis, headers=["one", "two", "three", "four", "five"]
        )

    datapoints = len(df.data) if axis == "row" else len(list(df.data.values())[0])
    assert datapoints == length
