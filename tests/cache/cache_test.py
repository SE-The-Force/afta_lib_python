import sys
# sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from afta_lib_python.cache.cache import Cache

class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache = Cache(2)

    def test_get_with_missing_key_should_return_default_value(self):
        defaultValue = lambda: "default"
        self.assertEqual(self.cache.get("key", defaultValue), "default")

    def test_get_with_existing_key_should_return_cached_value(self):
        self.cache.put("key", "value")
        defaultValue = lambda: "default"
        self.assertEqual(self.cache.get("key", defaultValue), "value")

    def test_put_when_cache_is_full_should_remove_oldest_entry(self):
        self.cache.put("key1", "value1")
        self.cache.put("key2", "value2")
        self.cache.put("key3", "value3")

        defaultValue = lambda: "default"
        self.assertEqual(self.cache.get("key1", defaultValue), "default")
        self.assertEqual(self.cache.get("key2", defaultValue), "value2")
        self.assertEqual(self.cache.get("key3", defaultValue), "value3")

if __name__ == '__main__':
    unittest.main()
