import sys
sys.path.insert(1, 'D:/School Stuff/5th Year - 2nd Sem/Project/afta_lib_python')

import math
from afta_lib_python.hits.hits import Hits

class TermQuery:
    def __init__(self, term):
        self.term = term

    async def search(self, indexer):
        ids, frequencies, doc_freqs = await indexer.database.search(self.term.text)
        documents = [await indexer.get_document(id) for id in ids]
        filteredDocuments = [doc for doc in documents if doc is not None]
        tf_idfs = {}
        totalDocs = await indexer.get_total_documents()
        for tf, index in zip(frequencies, range(len(frequencies))):
            idf = math.log(1 + (totalDocs / (1 + doc_freqs[index])))
            tf_idfs[ids[index]] = tf * idf
        sortedDocuments = sorted(filteredDocuments, key=lambda doc: tf_idfs[doc.id], reverse=True)
        return Hits(len(tf_idfs), sortedDocuments, tf_idfs)
