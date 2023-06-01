class Document:
    def __init__(self, id):
        self.id = id
        self.fields = []
        self.fieldMap = {}

    def add(self, field):
        self.fields.append(field)
        self.fieldMap[field.key] = field

    def getField(self, name):
        return self.fieldMap.get(name)

    def equals(self, other):
        if self is other:
            return True
        if not isinstance(other, Document):
            return False

        if self.id != other.id:
            return False
        return self.fieldsAreEqual(other)

    def hashCode(self):
        result = hash(self.id)
        result = 31 * result + self.fieldsHashCode()
        return result

    def fieldsHashCode(self):
        result = 1
        for field in self.fields:
            result = 31 * result + field.hashCode()
        return result

    def fieldsAreEqual(self, other):
        if len(self.fields) != len(other.fields):
            return False

        otherFieldsSet = set(other.fields)

        for field in self.fields:
            if field not in otherFieldsSet:
                return False

        return True
