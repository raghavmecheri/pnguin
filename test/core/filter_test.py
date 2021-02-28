import pytest
import json

import pnguin as pn


def _fetch_mock_payloads():
    arr = []

    with open("test/data/mockNumFilterData.json") as f:
        arr += json.load(f)

    with open("test/data/mockStrFilterData.json") as f:
        arr += json.load(f)

    return arr


CASES = _fetch_mock_payloads()


@pytest.mark.parametrize("payload", CASES)
def test_filter(payload):
    op, target, row, result = (
        payload["op"],
        payload["target"],
        payload["row"],
        payload["result"],
    )
    f = pn.Filter("test", op, target)
    assert f.does_conform(row) is result
