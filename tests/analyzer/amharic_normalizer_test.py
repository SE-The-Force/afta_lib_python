import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')
# 
import unittest
from afta_lib_python.analyzer.amharic_normalizer import AmharicNormalizer

class TestAmharicPreprocessor(unittest.TestCase):
    def setUp(self):
        self.normalizationTestcases = [
            ('ሀሐሓኅኻኃ', 'ሃሃሃሃሃሃ'),
            ('ዅሗኁኂ', 'ሁኋሁሂ'),
            ('ኄዄኅኆ', 'ሄሄሃሆ'),
            ('ሠሡሢሣሤሥሦ', 'ሰሱሲሳሴስሶ'),
            ('ዐዑዒዓኣዔዕዖ', 'አኡኢአአኤእኦ'),
            ('ፀፁጺጻጼፅፆ', 'ጸጹፂፃፄጽጾ')
        ]
        self.punctuationRemovalTestcases = [
            ('።።።', ''),
            ('እንደ : እንደ!',  'እንደ እንደ'),
            ('መልካም ጊዜ ነው።',  'መልካም ጊዜ ነው'),
            ('በለትተለት !እንቅስቃሴያችን @ውስጥ በድንገትና + ባላሰብነው ሁኔታ ከመለስተኛ አደጋዎች እስከ ከባድ የአጥንት መሰባበር ሊደርስብን #ይችላል፡፡', 
            'በለትተለት እንቅስቃሴያችን ውስጥ በድንገትና ባላሰብነው ሁኔታ ከመለስተኛ አደጋዎች እስከ ከባድ የአጥንት መሰባበር ሊደርስብን ይችላል'), 
            ('።፣፤፥፦፧፨',  '')
        ]
        self.stopwordRemovalTestcases = [
            ('እንደ እንደ', ''),
            ('አዲስ አበባ እንደ', 'አዲስ አበባ'),
            ('አዲስ አበባ', 'አዲስ አበባ'),
            ('አዲስ አበባ ተማ እና አዲስ አበባ ተማ', 'አዲስ አበባ ተማ አዲስ አበባ ተማ')
        ]
        self.extraSpaceRemovalTestcases = [
            ('አዲስ  አበባ', 'አዲስ አበባ'),
            ('  አዲስ አበባ  ', 'አዲስ አበባ'),
            ('አዲስ   አበባ', 'አዲስ አበባ'),
            ('አዲስ አበባ   እና   አዲስ አበባ', 'አዲስ አበባ እና አዲስ አበባ'),
            ('አዲስ አበባ', 'አዲስ አበባ'),
            ('አዲስ አበባ እና አዲስ አበባ', 'አዲስ አበባ እና አዲስ አበባ')
        ]
        self.mixedCharsTestCases = [
            ('አዲስ and አበባ 123', 'አዲስ አበባ'),
            ('አዲስ 1 አበባ 2', 'አዲስ አበባ'),
            ('አዲስ 123 አበባ', 'አዲስ አበባ'),
            ('hello አዲስ 123 world', 'አዲስ'),
            ('አዲስ 123 አበባ hello world', 'አዲስ አበባ')
        ]
        self.stemmerTestcases = [
            ('አዲስ', 'አድስ'),
            ('ሀብታሞቹ', 'ህብት'),
            ('ሀኪሞች', 'ህክ'),
            ('ሀይማኖትሽ', 'ህይምንት'),
        ]

    def test_normalize(self):
        for input_str, expected in self.normalizationTestcases:
            with self.subTest(input_str=input_str):
                result = AmharicNormalizer.normalize(input_str)
                self.assertEqual(result, expected)
        
    def test_punctuation_removal(self):
        for input_str, expected in self.punctuationRemovalTestcases:
            with self.subTest(input_str=input_str):
                result = AmharicNormalizer.remove_punctuation(input_str)
                self.assertEqual(result, expected)

    def test_stopword_removal(self):
        for input_str, expected in self.stopwordRemovalTestcases:
            with self.subTest(input_str=input_str):
                result = AmharicNormalizer.remove_stop_words(input_str)
                self.assertEqual(result, expected)

    def test_extra_space_removal(self):
        for input_str, expected in self.extraSpaceRemovalTestcases:
            with self.subTest(input_str=input_str):
                result = AmharicNormalizer.remove_extra_spaces(input_str)
                self.assertEqual(result, expected)

    def test_mixed_chars(self):
        for input_str, expected in self.mixedCharsTestCases:
            with self.subTest(input_str=input_str):
                result = AmharicNormalizer.remove_non_amharic_chars(input_str)
                self.assertEqual(result, expected)

    def test_stemmer(self):
        for input_str, expected in self.stemmerTestcases:
            with self.subTest(input_str=input_str):
                result = AmharicNormalizer.stem(input_str)
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

