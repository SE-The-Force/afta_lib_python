import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from afta_lib_python.parser.pdf_parser.pdf_parser import PdfParser

class TestPdfParser(unittest.TestCase):
    def setUp(self):
        self.parser = PdfParser("location")

    def test_is_stored(self):
        self.assertEqual(self.parser.is_stored("Book Title"), False)
        self.assertEqual(self.parser.is_stored("Page Number"), True)
        self.assertEqual(self.parser.is_stored("Content"), True)
        self.assertEqual(self.parser.is_stored("Other"), False)

    def test_is_indexable(self):
        self.assertEqual(self.parser.is_indexable("Book Title"), True)
        self.assertEqual(self.parser.is_indexable("Page Number"), False)
        self.assertEqual(self.parser.is_indexable("Content"), True)
        self.assertEqual(self.parser.is_indexable("Other"), False)

    def test_is_analyzed(self):
        self.assertEqual(self.parser.is_analyzed("Book Title"), False)
        self.assertEqual(self.parser.is_analyzed("Page Number"), False)
        self.assertEqual(self.parser.is_analyzed("Content"), True)
        self.assertEqual(self.parser.is_analyzed("Other"), False)

    def test_parse(self):
        temp_file_path = "./tests/pdf_parser/file2.pdf"
        parser = PdfParser(temp_file_path)
        data = parser.parse()
        # Check if the returned data matches the expected data from the PDF file
        self.assertEqual(data, [
            ["Book Title", "Page Number", "Content"],
            [temp_file_path, 1, "Test text page 1"],
            [temp_file_path, 2, "Test text page 2"],
        ])

if __name__ == '__main__':
    unittest.main()
