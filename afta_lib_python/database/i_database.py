from abc import ABC, abstractmethod

class IDatabase(ABC):
    @abstractmethod
    def insert(self, token, docId, position):
        pass

    @abstractmethod
    def search(self, token):
        pass

    @abstractmethod
    def save_document(self, document):
        pass

    @abstractmethod
    def get_document(self, id):
        pass
