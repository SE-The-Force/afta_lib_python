import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

from afta_lib_python.cache.cache import Cache

class IndexSearcher:
    def __init__(self, indexer):
        self.indexer = indexer
        self.search_cache = Cache(1000)

    async def search(self, query):
        return await self.search_cache.get(
            query,
            lambda: query.search(self.indexer)
        )
