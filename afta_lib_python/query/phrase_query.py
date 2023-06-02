import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

from afta_lib_python.query.query import Query
from afta_lib_python.hits.hits import Hits

class PhraseQuery(Query):
    def __init__(self, field, phrase):
        super().__init__()
        self.field = field
        self.phrase = phrase

    async def search(self, indexer):
        tokens = self.phrase.split(" ")
        hits = []
        documentIds = await indexer.database.search(self.phrase)
        documents = []
        for id in documentIds:
            doc = await indexer.get_document(id)
            documents.append(doc)
        for doc in documents:
            positions = {}
            if self.field in doc.fields:
                field_value = doc.fields[self.field]
                field_tokens = field_value.split(" ")
                for index, value in enumerate(field_tokens):
                    if value not in positions:
                        positions[value] = []
                    positions[value].append(index)
            found = True
            for i in range(1, len(tokens)):
                prev_token = tokens[i - 1]
                token = tokens[i]
                if (
                    prev_token not in positions
                    or token not in positions
                    or not any(p == q + 1 for p in positions[prev_token] for q in positions[token])
                ):
                    found = False
                    break
            if found:
                hits.append(doc)
        return Hits(len(hits), hits)
