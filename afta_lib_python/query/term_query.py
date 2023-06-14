import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import math
from afta_lib_python.hits.hits import Hits
from afta_lib_python.query.query import Query

"""
Class representing a Term Query.
Inherits Query
"""
class TermQuery(Query):

    """
    Create a Term Query.
    @param {string} term - The term to search for.
    """
    def __init__(self, term):
        self.term = term

    """
    Search the index using the Term query.
    @param {Indexer} indexer - The indexer instance.
    @returns {Hits} The search hits.
    """
    async def search(self, indexer, analyzer):
        analyzed_terms = await analyzer.analyze(self.term.text)
        term = analyzed_terms[0] if analyzed_terms else None
        doc_freqs = await indexer.database.get_num_docs_token_belongs_to(term)

        search_results = await indexer.database.search(term)
        ids, frequencies = search_results['ids'], search_results['frequencies']

        documents = await indexer.get_documents(ids)
        filtered_documents = list(filter(None, documents))

        # Compute tf-idf scores for each document
        tf_idfs = {}
        total_docs = await indexer.get_total_documents()
        for index, tf in enumerate(frequencies):
            idf = math.log(1 + (total_docs / (1 + doc_freqs)))
            tf_idfs[ids[index]] = tf * idf

        # Sort documents based on tf-idf scores
        filtered_documents.sort(key=lambda doc: tf_idfs[doc.id], reverse=True)
        
        # Create a Hits object
        return Hits(len(tf_idfs), filtered_documents, tf_idfs)
