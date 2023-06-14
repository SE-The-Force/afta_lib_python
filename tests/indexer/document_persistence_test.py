import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import pytest
import os
import time
from afta_lib_python.document.document import Document
from afta_lib_python.field.field import Field
from afta_lib_python.database.sqlite_database import SQLiteDatabase

class TestSQLiteDatabase:
    db = None
    db_name = None

    @pytest.fixture
    def setup_method_custom(self):
        # Setup steps to be executed before each test method
        self.db_name = f"test-{time.time()}.db"
        if os.path.exists(self.db_name):
            if self.db.open:
                self.db.close()
            os.unlink(self.db_name)
        self.db = SQLiteDatabase(self.db_name)
        self.db.create_tables()

    @pytest.mark.asyncio
    async def test_save_and_retrieve_documents(self, setup_method_custom):
        document = Document("doc2")
        document.add(Field("key", "value", "analyzed_value", True, True, True))

        await self.db.save_document(document)

        retrieved_document = await self.db.get_document("doc2")
        assert retrieved_document == document
   
    @pytest.mark.asyncio
    async def test_save_and_retrieve_multiple_documents(self, setup_method_custom):
        document1 = Document("doc1")
        document1.add(Field("key1", "value1", "analyzed_value1", True, True, True))
        await self.db.save_document(document1)

        document2 = Document("doc2")
        document2.add(Field("key2", "value2", "analyzed_value2", True, True, True))
        await self.db.save_document(document2)

        retrieved_document1 = await self.db.get_document("doc1")
        assert retrieved_document1 == document1

        retrieved_document2 = await self.db.get_document("doc2")
        assert retrieved_document2 == document2

    @pytest.mark.asyncio
    async def test_handle_documents_with_multiple_fields(self, setup_method_custom):
        document = Document("doc3")
        document.add(Field("key1", "value1", "analyzed_value1", True, True, True))
        document.add(Field("key2", "value2", "analyzed_value2", True, True, True))
        await self.db.save_document(document)

        retrieved_document = await self.db.get_document("doc3")
        assert retrieved_document == document

    @pytest.mark.asyncio
    async def test_search_documents(self, setup_method_custom):
        document = Document("doc4")
        document.add(Field("key", "value", "token", True, True, True))
        await self.db.save_document(document)
        await self.db.insert("token", "doc4", 0, 1)

        search_results = await self.db.search("token")
        expected_results = {
            "ids": ["doc4"],
            "frequencies": [1],
            "positions": [0]
        }
        assert search_results == expected_results
        # self.assertEqual(search_results, expected_results)

    # @pytest.mark.asyncio
    # async def test_handle_errors_correctly_when_creating_tables(self, setup_method_custom):
    #     old_run = self.db.db.run

    #     # Override the run method to simulate an error
    #     def run(sql, callback):
    #         callback(Exception("Test error"))

    #     self.db.db.run = run

    #     with self.assertRaisesRegex(Exception, "Test error"):
    #         await self.db.createTables()

    #     # Restore the original run method
    #     self.db.db.run = old_run
