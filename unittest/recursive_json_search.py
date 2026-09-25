from test_data import *
from policy import POLICY


def json_search(key, input_object, role=None):
    ret_val = []

    # Enforce role-based access control for protected keys
    if key in POLICY:
        allowed_roles = POLICY[key]

        if role not in allowed_roles:
            return []

    if isinstance(input_object, dict):
        for k, v in input_object.items():
            if k == key:
                temp = {k: v}
                ret_val.append(temp)

            if isinstance(v, dict):
                ret_val.extend(json_search(key, v, role))

            elif isinstance(v, list):
                for item in v:
                    if not isinstance(item, (str, int)):
                        ret_val.extend(json_search(key, item, role))

    elif isinstance(input_object, list):
        for val in input_object:
            if not isinstance(val, (str, int)):
                ret_val.extend(json_search(key, val, role))

    return ret_val


if __name__ == "__main__":
    print(json_search("issueSummary", data, role="viewer"))
