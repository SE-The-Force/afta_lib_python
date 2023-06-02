import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from afta_lib_python.term.term import Term
from afta_lib_python.query.phrase_query import PhraseQuery
from afta_lib_python.hits.hits import Hits

class TestPhraseQuery(unittest.TestCase):
    async def test_search_returns_hits_with_documents_containing_phrase_in_field(self):
        field = "field"
        phrase = "text1 text2"
        query = PhraseQuery(field, phrase)
        doc1 = {
            "id": 1,
            "fields": {
                field: "text1 text2",
            },
        }
        doc2 = {
            "id": 2,
            "fields": {
                field: "text1 text3",
            },
        }
        indexer = {
            "database": {
                "search": lambda phrase: [1],
            },
            "get_document": lambda id: doc1 if id == 1 else doc2,
        }
        expected_hits = Hits(1, [doc1])
        result = await query.search(indexer)
        self.assertEqual(result, expected_hits)

if __name__ == '__main__':
    unittest.main()
