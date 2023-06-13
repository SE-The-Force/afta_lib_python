import asyncio
import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

from afta_lib_python.query.query import Query
from afta_lib_python.hits.hits import Hits
from collections import defaultdict

class BooleanQuery(Query):
    def __init__(self, queries, operator):
        super().__init__()
        self.queries = queries
        self.operator = operator

    async def search(self, indexer, analyzer):
        hits_list = await self._search_queries(indexer, analyzer)
        if len(hits_list) == 0:
            return Hits(0, [])
            
        documents = []
        if self.operator == "AND":
            documents = self._perform_and_operation(hits_list)
        elif self.operator == "OR":
            documents = self._perform_or_operation(hits_list)
        else:
            raise ValueError(f"Invalid operator: {self.operator}")
            
        scores = self.combine_scores(hits_list, documents, self.operator)
        return Hits(len(documents), documents, scores)

    async def _search_queries(self, indexer, analyzer):
        hits_list = await asyncio.gather(*(query.search(indexer, analyzer) for query in self.queries))
        return hits_list

    def _perform_and_operation(self, hits_list):
        common_ids = set(hits.documents[0]["id"] for hits in hits_list)
        for hits in hits_list[1:]:
            current_ids = set(hits.documents[i]["id"] for i in range(len(hits_list)))
            common_ids = common_ids & current_ids
        
        common_documents = {doc["id"]: doc for hits in hits_list for doc in hits.documents if doc["id"] in common_ids}
        return list(common_documents.values())

    def _perform_or_operation(self, hits_list):
        all_documents = {doc["id"]: doc for hits in hits_list for doc in hits.documents}
        return list(all_documents.values())

    def combine_scores(self, hits_list, documents, operator):
        combined_scores = defaultdict(int)

        for document in documents:
            doc_id = document["id"]
            for hits in hits_list:
                if operator in ("AND", "OR") and doc_id in hits.scores:
                    combined_scores[doc_id] += hits.scores[doc_id]
                
        return combined_scores
