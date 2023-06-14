class Term:
    """
    Class representing a Term.
    """

    def __init__(self, field, text):
        """
        Create a Term.

        Parameters:
        field (str): The field associated with the term.
        text (str): The text of the term.
        """
        self.field = field
        self.text = text
