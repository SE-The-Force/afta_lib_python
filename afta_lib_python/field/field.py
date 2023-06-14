class Field:
    def __init__(self, key, value, analyzedValue="", isAnalyzed=False, isIndexible=False, isStored=False):
        """
        Create a Field instance.
        Args:
            key (str): The key of the field.
            value (str): The value of the field.
            analyzedValue (str): The analyzed value of the field.
            isAnalyzed (bool): A flag indicating whether the field is analyzed.
            isIndexible (bool): A flag indicating whether the field is indexible.
            isStored (bool): A flag indicating whether the field is stored.
        """
        self.key = key
        self.value = value
        self.analyzedValue = analyzedValue
        self.isAnalyzed = isAnalyzed
        self.isIndexible = isIndexible
        self.isStored = isStored

    def __hash__(self):
        """
        Compute the hash code for the field.
        Returns:
            int: The computed hash code.
        """
        result = hash(self.key)
        result = 31 * result + hash(self.value)
        result = 31 * result + hash(self.analyzedValue)
        result = 31 * result + hash(self.isAnalyzed)
        result = 31 * result + hash(self.isIndexible)
        result = 31 * result + hash(self.isStored)
        return result

    def __eq__(self, other):
        """
        Check if the field is equal to another field.
        Args:
            other (Field): The other field to compare with.
        
        Returns:
            bool: True if the fields are equal, false otherwise.
        """
        if self is other:
            return True
        if not isinstance(other, Field):
            return False
        return (
            self.key == other.key and
            self.value == other.value and
            self.analyzedValue == other.analyzedValue and
            self.isAnalyzed == other.isAnalyzed and
            self.isIndexible == other.isIndexible and
            self.isStored == other.isStored
        )
