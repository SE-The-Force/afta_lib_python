class Document:
    """
    Class representing a document.
    """
    def __init__(self, id):
        """
        Create a document.
        Args:
            id (str): The ID of the document.
        """
        self.id = id
        self.fields = []
        self.field_map = {}

    def add(self, field):
        """
        Add a field to the document.
        Args:
            field (Field): The field to add.
        """
        self.fields.append(field)
        self.field_map[field.key] = field

    def get_field(self, name):
        """
        Get a field from the document by name.
        Args:
            name (str): The name of the field.
        
        Returns:
            Field|None: The field with the specified name, or None if not found.
        """
        return self.field_map.get(name, None)

    def __eq__(self, other):
        """
        Check if the document is equal to another document.
        Args:
            other (Document): The other document to compare with.
        
        Returns:
            bool: True if the documents are equal, false otherwise.
        """
        if self is other:
            return True
        if not isinstance(other, Document):
            return False
        if self.id != other.id:
            return False
        return self.fields_are_equal(other)

    def __hash__(self):
        """
        Compute the hash code for the document.
        Returns:
            int: The computed hash code.
        """
        result = hash(self.id)
        result = 31 * result + self.fields_hash_code()
        return result

    def fields_hash_code(self):
        """
        Compute the hash code for the document's fields.
        Returns:
            int: The computed hash code.
        """
        result = 1
        for field in self.fields:
            result = 31 * result + hash(field)
        return result

    def fields_are_equal(self, other):
        """
        Check if the fields of the document are equal to the fields of another document.
        Args:
            other (Document): The other document to compare the fields with.
        
        Returns:
            bool: True if the fields are equal, false otherwise.
        """
        if len(self.fields) != len(other.fields):
            return False

        other_fields_set = set(other.fields)

        for field in self.fields:
            if field not in other_fields_set:
                return False

        return True
