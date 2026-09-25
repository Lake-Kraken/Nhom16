import unittest

from recursive_json_search import json_search
from test_data import data, key1, key2


class json_search_test(unittest.TestCase):
    '''Test module for json_search()'''

    def test_search_found(self):
        '''Authorized role should find an existing key'''
        self.assertTrue([] != json_search(key1, data, role="viewer"))

    def test_search_not_found(self):
        '''Missing key should return an empty list'''
        self.assertTrue([] == json_search(key2, data, role="viewer"))

    def test_is_a_list(self):
        '''json_search() should always return a list'''
        self.assertIsInstance(
            json_search(key1, data, role="viewer"),
            list
        )

    def test_viewer_cannot_read_api_key(self):
        '''Viewer must not be able to read apiKey'''
        result = json_search("apiKey", data, role="viewer")
        self.assertEqual([], result)

    def test_operator_cannot_read_api_key(self):
        '''Operator must not be able to read apiKey'''
        result = json_search("apiKey", data, role="operator")
        self.assertEqual([], result)

    def test_admin_can_read_api_key(self):
        '''Admin should be able to read apiKey'''
        result = json_search("apiKey", data, role="admin")
        self.assertNotEqual([], result)

    def test_viewer_cannot_read_management_ip(self):
        '''Viewer must not read managementIpAddress'''
        result = json_search(
            "managementIpAddress",
            data,
            role="viewer"
        )
        self.assertEqual([], result)

    def test_operator_can_read_management_ip(self):
        '''Operator should read managementIpAddress'''
        result = json_search(
            "managementIpAddress",
            data,
            role="operator"
        )
        self.assertNotEqual([], result)

    def test_invalid_role_cannot_read_api_key(self):
        '''Unknown roles must not access protected data'''
        result = json_search(
            "apiKey",
            data,
            role="invalid_role"
        )
        self.assertEqual([], result)


if __name__ == "__main__":
    unittest.main()
