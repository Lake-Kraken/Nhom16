import unittest

from recursive_json_search import json_search
from test_data import data


class json_search_test(unittest.TestCase):
    """Functional and security tests for recursive JSON search."""

    def test_search_found(self):
        """Search for a known nested key and ensure a value is returned."""
        result = json_search("status", data)
        self.assertIn("NEW", result)

    def test_search_not_found(self):
        """Search for a key that does not exist and ensure an empty list is returned."""
        result = json_search("missing_key", data)
        self.assertEqual(result, [])

    def test_is_a_list(self):
        """Verify that nested matches are aggregated into a list result."""
        nested_data = {
            "group": {
                "status": "open",
                "items": [{"status": "closed"}],
            }
        }
        result = json_search("status", nested_data)
        self.assertIsInstance(result, list)
        self.assertEqual(result, ["open", "closed"])

    def test_api_key_admin_access(self):
        """Admin users should be allowed to read the protected apiKey field."""
        self.assertEqual(json_search("apiKey", data, role="admin"), ["SNMP-COMMUNITY-STRING-7f3a9c"])

    def test_api_key_viewer_denied(self):
        """Viewer users must not receive protected apiKey values."""
        self.assertEqual(json_search("apiKey", data, role="viewer"), [])

    def test_management_ip_operator_allowed(self):
        """Operators are allowed to read managementIpAddress, while viewers are not."""
        allowed = json_search("managementIpAddress", data, role="operator")
        denied = json_search("managementIpAddress", data, role="viewer")
        self.assertEqual(allowed, ["10.10.20.21"])
        self.assertEqual(denied, [])

    def test_issue_summary_is_public(self):
        """Issue summaries should remain readable by all explicitly allowed roles."""
        for role in ["admin", "operator", "viewer"]:
            with self.subTest(role=role):
                self.assertIn("Network Device 10.10.20.82 Is Unreachable From Controller", json_search("issueSummary", data, role=role))

    def test_protected_default_deny(self):
        """Any missing or unauthorized role must be denied for protected keys."""
        self.assertEqual(json_search("apiKey", data, role=None), [])
        self.assertEqual(json_search("apiKey", data, role="guest"), [])


if __name__ == "__main__":
    unittest.main()

