import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from afta_lib_python.index_searcher.index_searcher import IndexSearcher
from afta_lib_python.query.query import Query
from afta_lib_python.hits.hits import Hits
from afta_lib_python.cache.cache import Cache

class TestIndexSearcher(unittest.TestCase):
    async def test_search_returns_result_from_cache_if_query_exists(self):
        indexer = {
            "getDocument": lambda id: None
        }
        query = Query()
        hits = Hits(1, [], 1)
        cache = Cache(1)
        cache.put(query, hits)
        searcher = IndexSearcher(indexer)
        searcher.search_cache = cache
        result = await searcher.search(query)
        self.assertEqual(result, hits)
        self.assertFalse(await query.search.called)
        await query.search.assert_called_once_with()

    async def test_search_calls_query_search_if_query_does_not_exist_in_cache(self):
        indexer = {
            "getDocument": lambda id: None
        }
        query = Query()
        hits = Hits(1, [], 1)
        query.search = lambda indexer: hits
        searcher = IndexSearcher(indexer)
        result = await searcher.search(query)
        self.assertEqual(result, hits)
        self.assertTrue(await query.search.called)
        self.assertEqual(await query.search.call_args[0][0], indexer)

if __name__ == '__main__':
    unittest.main()
