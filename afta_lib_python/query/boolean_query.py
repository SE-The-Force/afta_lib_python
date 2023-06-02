import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

from afta_lib_python.query.query import Query
from afta_lib_python.hits.hits import Hits

class BooleanQuery(Query):
    def __init__(self, queries, operator):
        super().__init__()
        self.queries = queries
        self.operator = operator

    async def search(self, indexer):
        hits_list = await self._search_queries(indexer)
        document_lists = [hits.documents for hits in hits_list]
        documents = []

        if self.operator == "AND":
            documents = self._perform_and_operation(document_lists)
        elif self.operator == "OR":
            documents = self._perform_or_operation(document_lists)
        elif self.operator == "NOT":
            documents = self._perform_not_operation(document_lists)
        else:
            raise ValueError(f"Invalid operator: {self.operator}")

        scores = self.combine_scores(hits_list, documents, self.operator)
        return Hits(len(documents), documents, scores)
    
    async def _search_queries(self, indexer):
        hits_list = []
        for query in self.queries:
            hits = await query.search(indexer)
            hits_list.append(hits)
        return hits_list

    def _perform_and_operation(self, document_lists):
        return list(set.intersection(*map(set, document_lists)))

    def _perform_or_operation(self, document_lists):
        return list(set.union(*map(set, document_lists)))

    def _perform_not_operation(self, document_lists):
        not_documents = set(document_lists[0])
        for docs in document_lists[1:]:
            not_documents -= set(docs)
        return list(not_documents)

    def combine_scores(self, hits_list, documents, operator):
        combined_scores = {}

        for document in documents:
            doc_id = document["id"]
            for hits in hits_list:
                if operator in ("AND", "OR"):
                    if doc_id in hits.scores:
                        combined_scores[doc_id] = combined_scores.get(doc_id, 0) + hits.scores[doc_id]
                elif operator == "NOT":
                    if hits is hits_list[0]:
                        if doc_id in hits.scores:
                            combined_scores[doc_id] = hits.scores[doc_id]
                    else:
                        if doc_id in hits.scores:
                            combined_scores[doc_id] -= hits.scores[doc_id]

        return combined_scores
