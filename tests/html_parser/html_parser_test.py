import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import pytest
from afta_lib_python.parser.html_parser.html_parser import HtmlParser

def test_is_stored():
    parser = HtmlParser("location")
    assert parser.is_stored("url") == True
    assert parser.is_stored("Content") == True
    assert parser.is_stored("Other") == False

def test_is_indexable():
    parser = HtmlParser("location")
    assert parser.is_indexable("url") == False
    assert parser.is_indexable("Content") == True
    assert parser.is_indexable("Other") == False

def test_is_analyzed():
    parser = HtmlParser("location")
    assert parser.is_analyzed("url") == False
    assert parser.is_analyzed("Content") == True
    assert parser.is_analyzed("Other") == False

@pytest.mark.asyncio
async def test_crawl():
    parser = HtmlParser("https://www.hanaelias.org", 2)
    data = await parser.crawl()
    assert len(data) > 0
