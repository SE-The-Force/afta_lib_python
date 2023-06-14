import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from unittest.mock import MagicMock
from afta_lib_python.term.term import Term
from afta_lib_python.query.term_query import TermQuery
# from afta_lib_python.hits.hits import Hits

class TestTermQuery(unittest.TestCase):
    async def test_search_returns_hits_with_documents_containing_term_text(self):
        term = Term("field", "text")
        query = TermQuery(term)
        doc1 = {"id": 1}
        doc2 = {"id": 2}
        indexer = {
            "getDocument": MagicMock(side_effect=lambda id: doc1 if id == 1 else doc2),
            "database": {
                "search": MagicMock(return_value={
                    "ids": [1, 2],
                    "frequencies": [2, 1],
                    "doc_freqs": [1, 1]
                }),
                "getTotalDocuments": MagicMock(return_value=2)
            },
            "getTotalDocuments": MagicMock(return_value=2)
        }

        hits = await query.search(indexer)
        
        self.assertEqual(hits.total_hits, 2)
        self.assertEqual(hits.documents, [doc1, doc2])
        self.assertGreater(hits.scores[doc1["id"]], hits.scores[doc2["id"]])
        indexer["getDocument"].assert_called_with(1)
        indexer["getDocument"].assert_called_with(2)
        indexer["database"]["search"].assert_called_with("text")
        indexer["getTotalDocuments"].assert_called_once()

if __name__ == "__main__":
    unittest.main()
