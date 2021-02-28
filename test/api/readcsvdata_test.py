import pytest
import json

import pnguin as pn


def _fetch_mock_payloads():
    with open("test/data/mockReadCsv.json") as f:
        return json.load(f)


@pytest.mark.parametrize("payload", [x for x in _fetch_mock_payloads()])
def test_read_csv_data(payload):
    path, length, need_headers = (
        payload["path"],
        payload["length"],
        payload["specifyHeaders"],
    )
    if not need_headers:
        data = pn.api.io.read_csv_to_data(path)
    else:
        data = pn.api.io.read_csv_to_data(
            path, headers=["one", "two", "three", "four", "five"]
        )
    assert len(data) == length
