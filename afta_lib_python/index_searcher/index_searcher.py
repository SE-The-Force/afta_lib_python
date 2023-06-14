import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

from afta_lib_python.cache.cache import Cache

class IndexSearcher:
    """
    Class representing an Index Searcher.
    """

    def __init__(self, indexer, analyzer):
        """
        Create an Index Searcher.

        Parameters:
        indexer (Indexer): The Indexer instance.
        analyzer (Analyzer): The Analyzer instance.
        """
        self.indexer = indexer
        self.analyzer = analyzer
        self.search_cache = Cache(1000)

    async def search(self, query):
        """
        Search the index for the specified query.

        Parameters:
        query (Query): The query to search with.

        Returns:
        Hits: A coroutine of the search hits.
        """
        return await self.search_cache.get(
            query,
            lambda: query.search(self.indexer, self.analyzer)
        )