import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import asynctest
from afta_lib_python.term.term import Term
from afta_lib_python.query.phrase_query import PhraseQuery
from afta_lib_python.hits.hits import Hits
from analyzer import Analyzer
from document import Document
from field import Field
from sqlite_database import SQLiteDatabase
from indexer import Indexer
from index_searcher import IndexSearcher
from pdf_parser import PdfParser

class TestPhraseQuery(asynctest.TestCase):

    async def test_search_returns_hits_with_documents_containing_phrase_in_field(self):
        analyzer = Analyzer("http://172.17.0.2:5000/analyze")
        db = SQLiteDatabase('phrase.db')
        await db.connect()
        indexer = Indexer(analyzer, db)
        searcher = IndexSearcher(indexer, analyzer)
        pdf_parser = PdfParser("./test/pdf_parser/file4.pdf")
        parsed_data = await pdf_parser.parse()

        for book_title, page_number, content in parsed_data[1:]:
            document = Document(f"{book_title}-{page_number}")
            document.add(
                Field(
                    "bookTitle",
                    book_title,
                    "",
                    pdf_parser.is_analyzed("Book Title"),
                    pdf_parser.is_stored("Book Title"),
                    pdf_parser.is_indexable("Book Title")
                )
            )
            document.add(
                Field(
                    "pageNumber",
                    str(page_number),
                    "",
                    pdf_parser.is_analyzed("Page Number"),
                    pdf_parser.is_stored("Page Number"),
                    pdf_parser.is_indexable("Page Number")
                )
            )
            document.add(
                Field(
                    "content",
                    content,
                    "",
                    pdf_parser.is_analyzed("Content"),
                    pdf_parser.is_stored("Content"),
                    pdf_parser.is_indexable("Content")
                )
            )
            await indexer.add_document(document)

        query1 = PhraseQuery(" ኢትዮጵያ ዘመን አቆጣጠር")
        query2 = PhraseQuery(" ኢትዮጵያ አቆጣጠር")

        hits1 = await query1.search(indexer, analyzer)
        hits2 = await query2.search(indexer, analyzer)

        self.assertGreater(hits1.total_hits, 0)
        self.assertEqual(hits2.total_hits, 0)


if __name__ == '__main__':
    asynctest.main()
