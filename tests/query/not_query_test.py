import asynctest
from term import Term
from not_query import NotQuery
from hits import Hits
from analyzer import Analyzer
from document import Document
from field import Field
from sqlite_database import SQLiteDatabase
from indexer import Indexer
from index_searcher import IndexSearcher
from pdf_parser import PdfParser


class TestNotQuery(asynctest.TestCase):

    async def test_not_query(self):
        analyzer = Analyzer("http://172.17.0.2:5000/analyze")
        db = SQLiteDatabase('not.db')
        await db.connect()
        indexer = Indexer(analyzer, db)
        searcher = IndexSearcher(indexer, analyzer)
        # Parse a PDF file using the PdfParser class
        pdf_parser = PdfParser("./test/pdf_parser/file4.pdf")
        parsed_data = await pdf_parser.parse()
        # Create a document for each page of the PDF file
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

        query1 = NotQuery("ኢትዮጵያ")
        query2 = NotQuery("ከበደ")
        
        hits1 = await query1.search(indexer, analyzer)
        hits2 = await query2.search(indexer, analyzer)
        
        self.assertEqual(hits1.total_hits, 0)
        self.assertGreater(hits2.total_hits, 0)


if __name__ == '__main__':
    asynctest.main()
