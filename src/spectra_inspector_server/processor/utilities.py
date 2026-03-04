def _get_nested_dict_element(d: dict, nested_keys: list[str] | str):

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
