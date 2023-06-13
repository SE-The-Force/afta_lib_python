import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')
from sets import Set
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

    async def search(self, indexer, analyzer):
        tokens = await analyzer.analyze(self.phrase)
        if len(tokens) == 0:
            return Hits(0, [])

        hits = []

        doc_ids_set = None
        docId_token_position = {}
        for token in tokens:
            result = await indexer.database.search(token)
            ids = result['ids']
            positions = result['positions']
            set1 = Set(ids)
            if not doc_ids_set:
                doc_ids_set = Set()
            else:
                doc_ids_set = doc_ids_set.intersection(set1)
            
            for i in range(len(ids)):
                docId = ids[i]
                if docId not in docId_token_position:
                    docId_token_position[docId][token] = Set()
                else:
                    docId_token_position[docId][token].add(positions[i])
        
        ts = tokens[1:]
        score = 0
        for docId in doc_ids_set:
            first = docId_token_position[docId][tokens[0]]
            found = True
            for startPoint in first:
                cur = startPoint
                found = True
                for token in ts:
                    if (cur + 1) in  docId_token_position[docId][token]:
                        cur = cur + 1
                    else:
                        found = False
                        break
                
                if found:
                    break
            
            if found:
                hits.append(await indexer.get_document(docId))

        return Hits(len(hits), hits) 