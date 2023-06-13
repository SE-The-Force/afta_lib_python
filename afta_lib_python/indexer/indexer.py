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

    async def add_all_documents(self, documents):
        for document in documents:
            self.document_cache.put(document.id, document)
        res = await self.indexAll(documents)
    
    async def get_documents(self, ids):
        res = await self.database.getDocuments(ids)
        return res;

    async def get_document_without_token(self, token):
        res = await self.database.getDocumentsWithoutToken(token)
        return res

    async def index_all(self, documents):
        fields_to_analyze = []
        for document in documents:
            for field in document.fields:
                if field.isIndexible and field.isAnalyzed:
                    fields_to_analyze.append(field.value)
        
        analyzed_tokens = await self.analyzer.analyze_all(fields_to_analyze)
        token_index = 0

        tuples = []
        for document in documents:
            for field in document.fields:
                if field.isIndexible:
                    tokens = [] 
                    if field.isAnalyzed:
                        tokens = analyzed_tokens[token_index]
                        token_index += 1
                    else:
                        tokens = field.value.split(" ")
                
                token_freq = {}
                for token in tokens:
                    if token not in token_freq:
                        token_freq[token] = 0
                    else:
                        token_freq[token] += 1
                
                for position, val in enumerate(tokens):
                    tuples.append((token,document.id, position, token_freq[token]))
        
        await self.database.inserAll(tuples)
        await self.database.saveAllDocuments(documents)


    async def get_document(self, id):
        if id in self.document_cache:
            pass
        res = await self.document_cache.get(
            id, lambda: self.database.get_document(id)
        )
        return res

    async def get_total_documents(self):
        return await self.database.get_total_documents()

    async def index(self, document):
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
