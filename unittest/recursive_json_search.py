from policy import POLICY


def _is_authorized(key, role):
    """Return True when the given role is allowed to access the protected key."""
    allowed_roles = POLICY.get(key, [])
    if not allowed_roles:
        return True
    if role is None:
        return False
    return role in allowed_roles


def json_search(key, input_object, role=None):
    """Recursively search nested dict/list structures for a target key and return matching values."""
    results = []

    if isinstance(input_object, dict):
        for current_key, value in input_object.items():
            if current_key == key:
                if _is_authorized(key, role):
                    results.append(value)
            nested_results = json_search(key, value, role=role)
            results.extend(nested_results)
    elif isinstance(input_object, list):
        for item in input_object:
            results.extend(json_search(key, item, role=role))

    return results

