import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import PyPDF2
from afta_lib_python.parser.parser import Parser
# from PyPDF2 import PdfFileReader
from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from pdfminer.high_level import extract_text


"""
Class representing a PDF Parser.
Extends Parser.
"""
class PdfParser(Parser):
    """
    Create a PDF Parser.
    @constructor
    @param {str} location - The location of the PDF file.
    """
    def __init__(self, location):
        super().__init__(location)

    """
    Check if the header is stored.
    @param {str} header - The header to check.
    @returns {bool} `True` if the header is stored, `False` otherwise.
    """
    def is_stored(self, header):
        if header == "Book Title":
            return False
        elif header == "Page Number":
            return True
        elif header == "Content":
            return True
        else:
            return False

    """
    Check if the header is indexable.
    @param {str} header - The header to check.
    @returns {bool} `True` if the header is indexable, `False` otherwise.
    """
    def is_indexable(self, header):
        if header == "Book Title":
            return True
        elif header == "Page Number":
            return False
        elif header == "Content":
            return True
        else:
            return False

    """
    Check if the header is analyzed.
    @param {str} header - The header to check.
    @returns {bool} `True` if the header is analyzed, `False` otherwise.
    """
    def is_analyzed(self, header):
        if header == "Book Title":
            return False
        elif header == "Page Number":
            return False
        elif header == "Content":
            return True
        else:
            return False

    """
    Parse the PDF file and extract the content.
    @returns {list[list[str]]} The parsed data as a 2D array.
    """
    def parse(self):
        data = [["Book Title", "Page Number", "Content"]]
        pdf_path = self.location
        with open(pdf_path, "rb") as file:
            pdf = PyPDF2.PdfReader(file)
            page_count = len(pdf.pages)
            for i in range(page_count):
                output_string = StringIO()
                extract_text_to_fp(file, output_string, laparams=LAParams(), page_numbers={i}, maxpages=0, caching=True)
                content = output_string.getvalue()
                cleaned_content = content.replace('\n\n\x0c', '').replace('\n\n', '').replace('\n', '').replace('\x0c', '')
                data.append([pdf_path, i + 1, cleaned_content])
        return data
    
    # def parse(self):
    #     data = [["Book Title", "Page Number", "Content"]]
    #     pdf_path = self.location

    #     with open(pdf_path, "rb") as file:
    #         pdf = PyPDF2.PdfReader(file)
    #         page_count = len(pdf.pages)
    #         print('count ', page_count)

    #         for i in range(page_count):
    #             page = pdf.pages[i]
    #             # page = pdf.getPage(i)
    #             content = page.extract_text()
    #             cleaned_content = content.replace('\n\n\x0c', '').replace('\n', '').replace('\x0c', '')
    #             data.append([pdf_path, i + 1, cleaned_content])

    #     return data
    
    # def parse(self):
    #     data = [["Book Title", "Page Number", "Content"]]
    #     pdf_path = self.location
    #     text = extract_text(pdf_path)
    #     lines = text.split("\n")
    #     page_count = len(lines)
    #     # for i in range(page_count):
    #     #     content = lines[1]
    #     #     data.append([pdf_path, i + 1, content])
    #     for i, content in enumerate(lines, start=1):
    #         if content:
    #             data.append([pdf_path, i, content])
    #     return data






