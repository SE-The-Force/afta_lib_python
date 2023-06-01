class Cache:
    def __init__(self, maxSize):
        self.maxSize = maxSize
        self.map = {}

    def get(self, key, defaultValue):
        return self.map.get(key, defaultValue())

    def put(self, key, value):
        if len(self.map) >= self.maxSize:
            oldestKey = next(iter(self.map))
            del self.map[oldestKey]
        self.map[key] = value
