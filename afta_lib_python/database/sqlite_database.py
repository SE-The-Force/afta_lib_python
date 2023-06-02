import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import sqlite3
from afta_lib_python.database.i_database import IDatabase
from afta_lib_python.document.document import Document
from afta_lib_python.field.field import Field

class SQLiteDatabase(IDatabase):
    def __init__(self, database_name):
        super().__init__()
        self.db = sqlite3.connect(database_name)

    async def connect(self):
        await self.create_tables()

    def close(self):
        self.db.close()

    async def create_tables(self):
        cursor = self.db.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS index_table (
            token TEXT, 
            doc_id TEXT, 
            position INTEGER,
            frequency INTEGER,
            doc_freq INTEGER)"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS documents_table (
            doc_id TEXT PRIMARY KEY)"""
        )

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS fields_table (
            key TEXT, 
            value TEXT, 
            analyzed_value TEXT, 
            is_analyzed INTEGER, 
            is_indexible INTEGER, 
            is_stored INTEGER, 
            doc_id TEXT)"""
        )

        self.db.commit()

    async def get_total_documents(self):
        cursor = self.db.cursor()

        cursor.execute(
            "SELECT COUNT(DISTINCT doc_id) as total FROM index_table"
        )

        result = cursor.fetchone()
        return result[0] if result else 0

    async def insert(self, token, doc_id, position, frequency):
        cursor = self.db.cursor()

        cursor.execute(
            "INSERT INTO index_table (token, doc_id, position, frequency) VALUES (?, ?, ?, ?)",
            (token, doc_id, position, frequency),
        )

        self.db.commit()

    async def search(self, token):
        cursor = self.db.cursor()

        cursor.execute(
            "SELECT doc_id, frequency, doc_freq FROM index_table WHERE token = ?",
            (token,),
        )

        rows = cursor.fetchall()
        ids = [row[0] for row in rows]
        frequencies = [row[1] for row in rows]
        doc_freqs = [row[2] for row in rows]

        return {"ids": ids, "frequencies": frequencies, "doc_freqs": doc_freqs}

    async def save_document(self, document):
        cursor = self.db.cursor()

        cursor.execute(
            "INSERT OR REPLACE INTO documents_table (doc_id) VALUES (?)",
            (document.id,),
        )

        for field in document.fields:
            cursor.execute(
                "INSERT INTO fields_table (key, value, analyzed_value, is_analyzed, is_indexible, is_stored, doc_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    field.key,
                    field.value,
                    field.analyzed_value,
                    int(field.is_analyzed),
                    int(field.is_indexible),
                    int(field.is_stored),
                    document.id,
                ),
            )

        self.db.commit()


    async def get_document(self, id):
        cursor = self.db.cursor()

        cursor.execute(
            "SELECT * FROM documents_table INNER JOIN fields_table ON documents_table.doc_id = fields_table.doc_id WHERE documents_table.doc_id = ?",
            (id,),
        )

        rows = cursor.fetchall()

        if len(rows) > 0:
            document = Document(id)
            for row in rows:
                field = Field(
                    row[2],
                    row[3],
                    row[4],
                    bool(row[5]),
                    bool(row[6]),
                    bool(row[7]),
                )
                document.add(field)

            return document

        return None
