#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch
from utils import get_json
from utils import memoize

class TestAccessNestedMap(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_

    Raises:
        Key: _description_
    """
    @parameterized.expand([
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a", ), {"b": 2}),
            ({"a": {"b":2}}, ("a", "b", ), 2)
            
        ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected, f"Accessing nested path {nested_map} should give {expected}")
    
    @parameterized.expand([
        ({}, ("a", ), "a"), 
        ({"a":1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        with self.assertRaises(KeyError, msg=f"Should raise Key error for the given {nested_map}, {path} and {expected}"):
            access_nested_map(nested_map, path)
            
class TestGetJson(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_

    Returns:
        _type_: _description_
    """
    @parameterized.expand(
        [
            ("example.com", "http//example.com", {"pay_load" : True}),
            ("holberton_io", "http//holberton_io", {"pay_load": False})
        ]
    )
    @patch("requests.get")
    def test_get_json(self, name, test_url, pay_load, mock_get):
        mock_get.return_value.json.return_value = pay_load
        self.assertEqual(get_json(test_url), pay_load, f"Should return payload for the {test_url} for {name}")     
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42
            @memoize
            def a_property(self):
                return self.a_method
            
        with patch.object(TestClass, 'a_method', return_value = 42)  as mock_method:
            test_obj = TestClass()
            self.assertEqual(test_obj.a_property(), 42)
            mock_method.assert_called_once()
            
if __name__ == "__main__":
    unittest.main()