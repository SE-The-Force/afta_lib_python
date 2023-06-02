import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

from afta_lib_python.cache.cache import Cache

class Indexer:
    def __init__(self, analyzer, database):
        self.analyzer = analyzer
        self.database = database
        self.document_cache = Cache(1000)

    async def add_document(self, document):
        self.document_cache.put(document.id, document)
        await self.index(document)

    async def get_document(self, id):
        if id in self.document_cache:
            pass
        res = await self.document_cache.get(
            id, lambda: self.database.get_document(id)
        )
        print("HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLLLLLL")
        return res

    async def get_total_documents(self):
        print("HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLLLLLL")
        return await self.database.get_total_documents()

    async def index(self, document):
        print("HEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEELLLLLLLLLLLLLLLLLLLLL")
        for field in document.fields:
            if field.isIndexible:
                tokens = field.value.split(" ")
                tokenFreq = {}
                for token in tokens:
                    if token not in tokenFreq:
                        tokenFreq[token] = 0
                    tokenFreq[token] += 1
                for position, token in enumerate(tokens):
                    await self.database.insert(token, document.id, position, tokenFreq[token])
        await self.database.save_document(document)
