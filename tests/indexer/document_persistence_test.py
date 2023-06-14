import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import unittest
from unittest.mock import Mock
import asyncio
import os
import time
from afta_lib_python.document.document import Document
from afta_lib_python.field.field import Field
from afta_lib_python.database.sqlite_database import SQLiteDatabase

# class TestSQLiteDatabase(unittest.TestCase):
#     def setUp(self):
#         self.dbName = f"test-{int(time.time())}.db"
#         self.loop = asyncio.get_event_loop()

#     def tearDown(self):
#         os.remove(self.dbName)

#     def test_save_and_retrieve_documents_correctly(self):
#         async def test():
#             db = SQLiteDatabase(self.dbName)
#             await db.connect()
#             await db.createTables()

#             document = Document("doc2")
#             document.add(Field("key", "value", "analyzed_value", True, True, True))
#             await db.saveDocument(document)

#             retrievedDocument = await db.getDocument("doc2")
#             self.assertEqual(retrievedDocument, document)

#             await db.close()

#         self.loop.run_until_complete(test())

#     # def test_save_and_retrieve_multiple_documents_correctly(self):
#     #     document1 = Document("doc1")
#     #     document1.add(Field("key1", "value1", "analyzed_value1", True, True, True))
#     #     self.loop.run_until_complete(self.db.saveDocument(document1))

#     #     document2 = Document("doc2")
#     #     document2.add(Field("key2", "value2", "analyzed_value2", True, True, True))
#     #     self.loop.run_until_complete(self.db.saveDocument(document2))

#     #     retrievedDocument1 = self.loop.run_until_complete(self.db.getDocument("doc1"))
#     #     self.assertEqual(retrievedDocument1, document1)

#     #     retrievedDocument2 = self.loop.run_until_complete(self.db.getDocument("doc2"))
#     #     self.assertEqual(retrievedDocument2, document2)

#     # def test_handle_documents_with_multiple_fields_correctly(self):
#     #     document = Document("doc3")
#     #     document.add(Field("key1", "value1", "analyzed_value1", True, True, True))
#     #     document.add(Field("key2", "value2", "analyzed_value2", True, True, True))
#     #     self.loop.run_until_complete(self.db.saveDocument(document))

#     #     retrievedDocument = self.loop.run_until_complete(self.db.getDocument("doc3"))
#     #     self.assertEqual(retrievedDocument, document)

#     # def test_search_for_documents_correctly(self):
#     #     document = Document("doc4")
#     #     document.add(Field("key", "value", "token", True, True, True))
#     #     self.loop.run_until_complete(self.db.saveDocument(document))
#     #     self.loop.run_until_complete(self.db.insert("token", "doc4", 0))

#     #     searchResults = self.loop.run_until_complete(self.db.search("token"))
#     #     expectedResults = {
#     #         "ids": ["doc4"],
#     #         "frequencies": [None],
#     #         "doc_freqs": [None]
#     #     }
#     #     self.assertEqual(searchResults, expectedResults)

#     # def test_handle_errors_correctly_when_creating_tables(self):
#         old_run = self.db.db.run

#         # Override the run method to simulate an error
#         def run_with_error(sql, callback):
#             callback(Exception("Test error"))

#         self.db.db.run = Mock(side_effect=run_with_error)

#         with self.assertRaisesRegex(Exception, "Test error"):
#             self.loop.run_until_complete(self.db.createTables())

#         # Restore the original run method
#         self.db.db.run = old_run

# if __name__ == '__main__':
#     unittest.main()

class TestSQLiteDatabase(unittest.TestCase):
    def setUp(self):
        self.db = None
        self.db_name = None

    def tearDown(self):
        if self.db_name and os.path.exists(self.db_name):
            if self.db:
                self.db.close()
            os.unlink(self.db_name)

    async def test_save_and_retrieve_documents(self):
        self.db_name = f"test-{int(time.time())}.db"
        
        if os.path.exists(self.db_name):
            os.unlink(self.db_name)

        self.db = SQLiteDatabase(self.db_name)
        await self.db.create_tables()

        document = Document("doc2")
        document.add(Field("key", "value", "analyzed_value", True, True, True))
        await self.db.save_document(document)

        retrieved_document = await self.db.get_document("doc2")
        self.assertEqual(retrieved_document, document)

    async def test_save_and_retrieve_multiple_documents(self):
        self.db_name = f"test-{int(time.time())}.db"
        
        if os.path.exists(self.db_name):
            os.unlink(self.db_name)

        self.db = SQLiteDatabase(self.db_name)
        await self.db.create_tables()

        document1 = Document("doc1")
        document1.add(Field("key1", "value1", "analyzed_value1", True, True, True))
        await self.db.save_document(document1)

        document2 = Document("doc2")
        document2.add(Field("key2", "value2", "analyzed_value2", True, True, True))
        await self.db.save_document(document2)

        retrieved_document1 = await self.db.get_document("doc1")
        self.assertEqual(retrieved_document1, document1)

        retrieved_document2 = self.db.get_document("doc2")
        self.assertEqual(retrieved_document2, document2)

    async def test_handle_documents_with_multiple_fields(self):
        self.db_name = f"test-{int(time.time())}.db"
        
        if os.path.exists(self.db_name):
            os.unlink(self.db_name)

        self.db = SQLiteDatabase(self.db_name)
        await self.db.create_tables()

        document = Document("doc3")
        document.add(Field("key1", "value1", "analyzed_value1", True, True, True))
        document.add(Field("key2", "value2", "analyzed_value2", True, True, True))
        await self.db.save_document(document)

        retrieved_document = await self.db.get_document("doc3")
        self.assertEqual(retrieved_document, document)

    async def test_search_documents(self):
        self.db_name = f"test-{int(time.time())}.db"
        
        if os.path.exists(self.db_name):
            os.unlink(self.db_name)

        self.db = SQLiteDatabase(self.db_name)
        await self.db.create_tables()

        document = Document("doc4")
        document.add(Field("key", "value", "token", True, True, True))
        await self.db.save_document(document)
        self.db.insert("token", "doc4", 0)

        search_results = await self.db.search("token")

        expected_results = {
            "ids": ["doc4"],
            "frequencies": [None],
            "doc_freqs": [None]
        }
        self.assertEqual(search_results, expected_results)

    async def test_handle_errors_correctly_when_creating_tables(self):
        self.db_name = f"test-{int(time.time())}.db"
        
        if os.path.exists(self.db_name):
            os.unlink(self.db_name)

        self.db = SQLiteDatabase(self.db_name)
        await self.db.create_tables()

        old_run = self.db.db.run

        # Override the run method to simulate an error
        def run(sql, callback):
            callback(Exception("Test error"))

        self.db.db.run = run

        with self.assertRaisesRegex(Exception, "Test error"):
            await self.db.createTables()

        # Restore the original run method
        self.db.db.run = old_run


if __name__ == "__main__":
    unittest.main()