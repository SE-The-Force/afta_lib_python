import sys
# sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from afta_lib_python.analyzer.analyzer import AnalyzerMock

class TestAnalyzerMock(unittest.TestCase):
    def test_split_text_into_tokens(self):
        analyzer = AnalyzerMock()

        text = 'This is a test'
        result = analyzer.tokens(text)

        self.assertEqual(result, ['This', 'is', 'a', 'test'])

    def test_normalize_and_analyze_text(self):
        analyzer = AnalyzerMock()

        text = 'ይህ ምርመራ ነው'
        result = analyzer.analyze(text)

if __name__ == "__main__":
    unittest.main()
