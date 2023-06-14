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

    def create_tables(self):
        cursor = self.db.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS index_table (
            token TEXT, 
            doc_id TEXT, 
            position INTEGER,
            frequency INTEGER)"""
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

    async def get_num_docs_token_belongs_to(self, token):
        cursor = self.db.cursor()
        self.execute("""
            SELECT COUNT(DISTINCT doc_id) as num_docs FROM index_table WHERE token = ?
        """, (token,))

        result = cursor.fetchone()
        return result[0] if result else 0


    async def insertAll(self, data):
        try:
            self.db.execute('BEGIN TRANSACTION')

            for row in data:
                self.db.execute('INSERT INTO index_table (token, doc_id, position, frequency) VALUES (?, ?, ?, ?)', row)

            self.db.commit()

        except sqlite3.Error as err:
            print(f"An error occurred: {err}")

        return



    async def search(self, token):
        try:
            cursor = self.db.execute("SELECT doc_id, frequency, position FROM index_table WHERE token = ?", (token,))
            rows = cursor.fetchall()

            ids = [row[0] for row in rows]
            frequencies = [row[1] for row in rows]
            positions = [row[2] for row in rows]

            return {'ids': ids, 'frequencies': frequencies, 'positions': positions}

        except sqlite3.Error as err:
            print(f"An error occurred: {err}")

    async def get_documents_without_token(self,token):
        try:
            cursor = self.db.execute("""
                SELECT * FROM documents_table 
                WHERE NOT EXISTS (
                    SELECT 1 FROM index_table 
                    WHERE documents_table.doc_id = index_table.doc_id 
                    AND index_table.token = ?
                )
            """, (token,))
            rows = cursor.fetchall()

            documents = []
            for row in rows:
                document = await self.get_document(row[0])  # assuming this function exists
                documents.append(document)

            return documents
        except sqlite3.Error as err:
            print(f"An error occurred: {err}")

    async def save_all_documents(self, documents):
        try:
            self.db.execute("BEGIN TRANSACTION")

            for document in documents:
                self.db.execute("INSERT OR REPLACE INTO documents_table (doc_id) VALUES (?)", (document['id'],))

                for field in document['fields']:
                    self.db.execute("""
                        INSERT INTO fields_table (key, value, analyzed_value, is_analyzed, is_indexible, is_stored, doc_id) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (field['key'], field['value'], field['analyzedValue'], int(field['isAnalyzed']), 
                          int(field['isIndexible']), int(field['isStored']), document['id']))

            self.db.commit()
        except sqlite3.Error as err:
            self.db.execute("ROLLBACK")
            print(f"An error occurred: {err}")

    async def get_documents(self, ids):
        try:
            id_string = ",".join('?' for _ in ids)
            cursor = self.db.execute(f"""
                SELECT * FROM documents_table 
                INNER JOIN fields_table ON documents_table.doc_id = fields_table.doc_id 
                WHERE documents_table.doc_id IN ({id_string})
            """, ids)
            rows = cursor.fetchall()

            # Assuming Document and Field classes are defined somewhere
            docs = {}
            for row in rows:
                if row['doc_id'] not in docs:
                    docs[row['doc_id']] = Document(row['doc_id'])

                field = Field(row['key'], row['value'], row['analyzed_value'], bool(row['is_analyzed']),
                              bool(row['is_indexible']), bool(row['is_stored']))
                docs[row['doc_id']].add(field)

            return list(docs.values())
        except sqlite3.Error as err:
            print(f"An error occurred: {err}")


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
                    field.analyzedValue,
                    int(field.isAnalyzed),
                    int(field.isIndexible),
                    int(field.isStored),
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
                    row[1],
                    row[2],
                    row[3],
                    bool(row[4]),
                    bool(row[5]),
                    bool(row[6]),
                )
                document.add(field)
            return document

        return None
