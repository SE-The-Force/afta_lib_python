import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

from afta_lib_python.indexer.indexer import Indexer
from afta_lib_python.document.document import Document
from afta_lib_python.field.field import Field
from afta_lib_python.analyzer.analyzer import AnalyzerMock
import unittest
import asyncio

class MockDatabase:
    async def initialize(self):
        pass

    async def query(self):
        return [{"id": 1, "name": "John"}]

    async def close(self):
        pass

    async def create_tables(self):
        pass

    async def insert(self):
        pass

    async def search(self):
        return ["doc1", "doc2"]

    async def save_document(self):
        pass

    async def get_document(self):
        return {"id": "doc1", "fields": []}

class TestIndexer(unittest.TestCase):
    def setUp(self):
        self.analyzerMock = AnalyzerMock()
        self.mockDatabase = MockDatabase()

    async def test_add_document_to_index(self):
        indexer = Indexer(self.analyzerMock, self.mockDatabase)
        document = Document("testId")
        field = Field("key", "value1 value2", "", False, True, True)

        document.add(field)
        await indexer.add_document(document)

        retrievedDocument = await indexer.get_document("testId")
        
        print(retrievedDocument.fields[0].value, document.fields[0].value)
        self.assertEqual(retrievedDocument.fields[0].value, document.fields[0].value)

    async def test_retrieve_document_from_cache(self):
        indexer = Indexer(self.analyzerMock, self.mockDatabase)
        document = Document("testId")
        field = Field("key", "value1 value2", "", False, True, True)

        document.add(field)
        await indexer.add_document(document)

        cachedDocument = await indexer.get_document("testId")
        self.assertEqual(cachedDocument, document)

    # # Add this method to run the async tests
    # def run_async(self, coro):
    #     loop = asyncio.get_event_loop()
    #     return loop.run_until_complete(coro)

    # # Override the runTest method to run the async tests
    # def runTest(self):
    #     self.run_async(self.test_add_document_to_index())
    #     self.run_async(self.test_retrieve_document_from_cache())

if __name__ == "__main__":
    unittest.main()
