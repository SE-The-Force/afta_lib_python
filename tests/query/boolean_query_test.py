import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from unittest.mock import MagicMock

from afta_lib_python.term.term import Term
from afta_lib_python.query.boolean_query import BooleanQuery
from afta_lib_python.hits.hits import Hits

class TestBooleanQuery(unittest.TestCase):
    def setUp(self):
        self.indexer = MagicMock()

    async def test_search_returns_correct_documents_for_AND_operator(self):
        doc1 = {"id": 1, "score": 1.5}
        doc2 = {"id": 2, "score": 2.5}
        doc3 = {"id": 3, "score": 1.0}

        query1 = MagicMock()
        query1.search.return_value = Hits(2, [doc1, doc2], {"1": 1.5, "2": 2.5})

        query2 = MagicMock()
        query2.search.return_value = Hits(2, [doc2, doc3], {"2": 2.5, "3": 1.0})

        boolean_query = BooleanQuery([query1, query2], "AND")
        result = await boolean_query.search(self.indexer)

        self.assertEqual(result.documents, [doc2])  # doc2 is in both queries
        self.assertEqual(result.scores, {"2": 5.0})  # doc2 score is the sum of query1 and query2 scores

    async def test_search_returns_correct_documents_for_OR_operator(self):
        doc1 = {"id": 1, "score": 1.5}
        doc2 = {"id": 2, "score": 2.5}
        doc3 = {"id": 3, "score": 1.0}

        query1 = MagicMock()
        query1.search.return_value = Hits(2, [doc1, doc2], {"1": 1.5, "2": 2.5})

        query2 = MagicMock()
        query2.search.return_value = Hits(2, [doc2, doc3], {"2": 2.5, "3": 1.0})

        boolean_query = BooleanQuery([query1, query2], "OR")
        result = await boolean_query.search(self.indexer)

        self.assertEqual(result.documents, [doc1, doc2, doc3])  # All documents are returned
        self.assertEqual(result.scores, {"1": 1.5, "2": 5.0, "3": 1.0})  # Scores are summed where applicable

    async def test_search_returns_correct_documents_for_NOT_operator(self):
        doc1 = {"id": 1, "score": 1.5}
        doc2 = {"id": 2, "score": 2.5}
        doc3 = {"id": 3, "score": 1.0}

        query1 = MagicMock()
        query1.search.return_value = Hits(2, [doc1, doc2], {"1": 1.5, "2": 2.5})

        query2 = MagicMock()
        query2.search.return_value = Hits(2, [doc2, doc3], {"2": 2.5, "3": 1.0})

        boolean_query = BooleanQuery([query1, query2], "NOT")
        result = await boolean_query.search(self.indexer)

        self.assertEqual(result.documents, [doc1])  # doc1 is only in the first query
        self.assertEqual(result.scores, {"1": 1.5})  # doc2 score is not included

if __name__ == "__main__":
    unittest.main()
