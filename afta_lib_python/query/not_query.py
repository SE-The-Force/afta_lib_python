import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')
import asyncio
from afta_lib_python.query.query import Query
from afta_lib_python.hits.hits import Hits

class NotQuery(Query):
    """
    Class representing a Not Query.
    Extends Query class.
    """

    def __init__(self, query):
        """
        Create a Not Query.

        Parameters:
        query (str): The queries to combine.
        """
        super().__init__()
        self.query = query

    async def search(self, indexer, analyzer):
        """
        Search the index using the Not query.

        Parameters:
        indexer (Indexer): The indexer instance.
        analyzer (Analyzer): The analyzer instance.

        Returns:
        Hits: An object representing the search hits.
        """
        tokens = await analyzer.analyze(self.query)
        batches = await asyncio.gather(*(indexer.get_documents_without_token(token) for token in tokens))
        if not batches:
            return Hits(0, [], {})

        common_ids = set(doc.id for doc in batches[0])
        for batch in batches[1:]:
            current_ids = set(doc.id for doc in batch)
            common_ids = common_ids.intersection(current_ids)

        common_documents = {}
        scores = {}
        for batch in batches:
            for doc in batch:
                if doc.id in common_ids:
                    common_documents[doc.id] = doc
                    scores[doc.id] = 0

        result = list(common_documents.values())
        return Hits(len(result), result, scores)
