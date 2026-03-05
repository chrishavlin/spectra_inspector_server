from spectra_inspector_server.processor.utilities import _get_nested_dict_element


def test_get_nested_dict_element() -> None:

    d = {"a": {"b": {"c": 1}}, "d": 2, "e": {"f": 3}}

    assert _get_nested_dict_element(d, ["a", "b", "c"]) == 1
    assert _get_nested_dict_element(d, "d") == 2
    assert _get_nested_dict_element(d, ["e", "f"]) == 3

    dval = _get_nested_dict_element(d, ["a", "b"])
    assert isinstance(dval, dict)
    assert dval["c"] == 1
