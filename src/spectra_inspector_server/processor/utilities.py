from typing import Any


def _get_nested_dict_element(d: dict[str, Any], nested_keys: list[str] | str) -> Any:
    """Given a dictionary with nested dictionaries, this returns a nested value.


    e.g., given

    a = {'b': {'c': {'d': 0}}}

    then

    _get_nested_dict_element(a, ('b', 'c', 'd')) will return the equivalent of
    a['b']['c']['d'] (in this case, 0).


    Parameters
    ----------
    d : dict
        the dictionary to inspect
    nested_keys : list[str] | str
        the nested keys

    Returns
    -------
    Any
        Whatever the nested value may be.

    Raises
    ------
    KeyError
        If a key is accessed that does not exist
    """

    if isinstance(nested_keys, str):
        nested_keys = [nested_keys]

    if nested_keys[0] in d:
        if isinstance(d[nested_keys[0]], dict):
            if len(nested_keys) == 1:
                return d[nested_keys[0]]
            # go deeper
            new_list = nested_keys[1:]
            return _get_nested_dict_element(d[nested_keys[0]], new_list)
        return d[nested_keys[0]]

    msg = f"{nested_keys[0]} is not in dictionary"
    raise KeyError(msg)
