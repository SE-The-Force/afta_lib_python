import sys
# sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from afta_lib_python.analyzer.amharic_normalizer import AmharicNormalizer

class AmharicNormalizerTestCase(unittest.TestCase):
    def test_normalize(self):
        tests = [
            {'input': 'ሀሐሓኅኻኃ', 'expected': 'ሃሃሃሃሃሃ'},
            {'input': 'ዅሗኁኂ', 'expected': 'ሁኋሁሂ'},
            {'input': 'ኄዄኅኆ', 'expected': 'ሄሄሃሆ'},
            {'input': 'ሠሡሢሣሤሥሦ', 'expected': 'ሰሱሲሳሴስሶ'},
            {'input': 'ዐዑዒዓኣዔዕዖ', 'expected': 'አኡኢአአኤእኦ'},
            {'input': 'ፀፁጺጻጼፅፆ', 'expected': 'ጸጹፂፃፄጽጾ'}
        ]
        
        for test in tests:
            input_text = test['input']
            expected_output = test['expected']
            result = AmharicNormalizer.normalize(input_text)
            self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()
