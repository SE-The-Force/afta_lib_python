class Hits:
    """
    Class representing search hits.
    """
    def __init__(self, total_hits, documents, scores):
        """
        Create search hits.

        Parameters:
        total_hits (int): The total number of hits.
        documents (list): The list of Document objects representing the hits.
        scores (list): The list of scores for each hit (based on tf-idf).
        """
        self.total_hits = total_hits
        self.documents = documents
        # The score is based on tf-idf
        self.scores = scores
