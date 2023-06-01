class Field:
    def __init__(self, key, value, analyzedValue="", isAnalyzed=False, isIndexible=False, isStored=False):
        self.key = key
        self.value = value
        self.analyzedValue = analyzedValue
        self.isAnalyzed = isAnalyzed
        self.isIndexible = isIndexible
        self.isStored = isStored

    def hashCode(self):
        result = hash(self.key)
        result = 31 * result + hash(self.value)
        result = 31 * result + hash(self.analyzedValue)
        result = 31 * result + hash(self.isAnalyzed)
        result = 31 * result + hash(self.isIndexible)
        result = 31 * result + hash(self.isStored)
        return result
