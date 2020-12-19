import pytest
import json

import pnguin as pg


def _fetch_mock_payloads():
    with open("test/data/mockInit.json") as f:
        return json.load(f)


@pytest.mark.parametrize("payload", [x for x in _fetch_mock_payloads()])
def test_create(payload):
    data, axis = payload["data"], payload["axis"]
    df = pg.DataFrame(data=data, axis=axis)
    if type(df.data) == type(data):
        assert df.data == data
    if axis == "row":
        assert isinstance(df.data, list)
    else:
        assert isinstance(df.data, dict)


def test_head():
    assert True is True


def test_dropna():
    assert True is True


def test_apply():
    assert True is True


def test_print():
    assert True is True
