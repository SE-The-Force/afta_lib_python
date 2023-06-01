import sys
# sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from afta_lib_python.document.document import Document
from afta_lib_python.field.field import Field

class DocumentTestCase(unittest.TestCase):
    # should add fields to the document
    def test_document_add_fields(self):
        document = Document(1)
        field1 = Field("field1", "value1", "analyzedValue1", True, True, True)
        field2 = Field("value2", "analyzedValue2", False, False, False)
        document.add(field1)
        document.add(field2)
        self.assertEqual(document.fields, [field1, field2])

    # should return true when comparing two documents with the same id and fields
    def test_document_compare_same_id_and_fields(self):
        document1 = Document(1)
        field1 = Field("field1", "value1", "analyzedValue1", True, True, True)
        field2 = Field("field2", "value2", "analyzedValue2", True, True, True)
        document1.add(field1)
        document1.add(field2)

        document2 = Document(1)
        document2.add(field1)
        document2.add(field2)

        self.assertTrue(document1.equals(document2))

    # should return false when comparing two documents with different ids
    def test_document_compare_different_ids(self):
        document1 = Document(1)
        document2 = Document(2)

        self.assertFalse(document1.equals(document2))

    # should return false when comparing two documents with different fields
    def test_document_compare_different_fields(self):
        document1 = Document(1)
        field1 = Field("field1", "value1")
        document1.add(field1)

        document2 = Document(1)
        field2 = Field("field2", "value2")
        document2.add(field2)

        self.assertFalse(document1.equals(document2))

    # should return false when comparing two documents with different number of fields
    def test_document_compare_different_number_of_fields(self):
        document1 = Document(1)
        field1 = Field("field1", "value1")
        document1.add(field1)

        document2 = Document(1)
        field2 = Field("field2", "value2")
        field3 = Field("field3", "value3")
        document2.add(field2)
        document2.add(field3)

        self.assertFalse(document1.equals(document2))

    # should return false when comparing a document to a non-document object
    def test_document_compare_to_non_document_object(self):
        document = Document(1)
        self.assertFalse(document.equals({}))

    # should return the same hash code for two documents with the same id and fields
    def test_document_same_hash_code_for_same_id_and_fields(self):
        document1 = Document(1)
        field1 = Field("field1", "value1", "analyzedValue1", True, True, True)
        field2 = Field("field2", "value2", "analyzedValue2", True, True, True)
        document1.add(field1)
        document1.add(field2)

        document2 = Document(1)
        document2.add(field1)
        document2.add(field2)

        self.assertEqual(document1.hashCode(), document2.hashCode())

    # should return true when comparing two documents with the same fields in different orders
    def test_document_compare_same_fields_in_different_orders(self):
        document1 = Document(1)
        field1 = Field("field1", "value1")
        field2 = Field("field2", "value2")
        document1.add(field1)
        document1.add(field2)

        document2 = Document(1)
        document2.add(field2)
        document2.add(field1)

        self.assertTrue(document1.equals(document2))

    # should return true when comparing a document to itself
    def test_document_compare_to_itself(self):
        document = Document(1)
        self.assertTrue(document.equals(document))

if __name__ == "__main__":
    unittest.main()
