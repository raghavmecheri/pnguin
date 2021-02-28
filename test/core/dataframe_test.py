import pytest
import json

import pnguin as pn


def _fetch_mock_payloads():
    with open("test/data/mockInit.json") as f:
        return json.load(f)


def _fetch_mock_filter_payloads():
    with open("test/data/mockFilters.json") as f:
        return json.load(f)


def _nanify(payload):
    def _modify(x):
        if isinstance(x, dict):
            x["name"] = ["Raghav", float("NaN")]
            return x, 1
        else:
            x[1] = {
                "name": float("NaN"),
                "occupation": "Bored2",
                "message": "Another one",
            }
            return x, 1

    axis, data = payload["axis"], payload["data"]
    mod_data, clean_len = _modify(data)
    return {"axis": axis, "data": mod_data, "clean_len": clean_len}


@pytest.mark.parametrize("payload", [x for x in _fetch_mock_payloads()])
def test_create(payload):
    data, axis = payload["data"], payload["axis"]
    df = pn.DataFrame(data=data, axis=axis)
    if type(df.data) == type(data):
        assert df.data == data
    if axis == "row":
        assert isinstance(df.data, list)
    else:
        assert isinstance(df.data, dict)


@pytest.mark.parametrize("payload", [x for x in _fetch_mock_payloads()])
def test_head(payload):
    def _eval_head(head, original_len, x):
        assert len(head._data_as_rows()) == (x if original_len > x else original_len)

    data, axis = payload["data"], payload["axis"]
    df = pn.DataFrame(data=data, axis=axis)
    ranges = [1, 2, 3, 4, 5]
    for r in ranges:
        original_len = (
            len(data) if isinstance(data, list) else len(next(iter(data.values())))
        )
        _eval_head(df.head(n=r), original_len, r)


@pytest.mark.parametrize("payload", [_nanify(x) for x in _fetch_mock_payloads()])
def test_dropna(payload):
    data, clean_len, axis = payload["data"], payload["clean_len"], payload["axis"]
    df = pn.DataFrame(data=data, axis=axis).dropna()
    rows = df._data_as_rows()
    assert len(rows) is clean_len


@pytest.mark.parametrize("payload", [x for x in _fetch_mock_filter_payloads()])
def test_filter(payload):
    data, op, target, length, axis = (
        payload["data"],
        payload["op"],
        payload["target"],
        payload["length"],
        payload["axis"],
    )
    df = pn.DataFrame(data=data, axis=axis)
    f = pn.Filter("test", op, target)
    res = df.filter(f)
    assert len(res.data) is length


def test_apply():
    assert True is True


@pytest.mark.parametrize("payload", [_nanify(x) for x in _fetch_mock_payloads()])
def test_tostring(payload):
    data, axis = payload["data"], payload["axis"]
    df = pn.DataFrame(data=data, axis=axis)
    x = df._to_string()
    assert x is not None
