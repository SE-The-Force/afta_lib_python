import sys
# sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from afta_lib_python.field.field import Field

class FieldTestCase(unittest.TestCase):
    def test_field_properties(self):
        field = Field("key", "value", "analyzedValue", True, True, True)

        self.assertEqual(field.key, "key")
        self.assertEqual(field.value, "value")
        self.assertEqual(field.analyzedValue, "analyzedValue")
        self.assertEqual(field.isAnalyzed, True)
        self.assertEqual(field.isIndexible, True)
        self.assertEqual(field.isStored, True)

    def test_field_default_properties(self):
        field = Field("key", "value")

        self.assertEqual(field.analyzedValue, "")
        self.assertEqual(field.isAnalyzed, False)
        self.assertEqual(field.isIndexible, False)
        self.assertEqual(field.isStored, False)

if __name__ == '__main__':
    unittest.main()
