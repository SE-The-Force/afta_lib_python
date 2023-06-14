from collections import OrderedDict

class Cache:
    """
    Class representing a cache.
    """
    def __init__(self, max_size):
        """
        Create a cache.
        Args:
            max_size (int): The maximum size of the cache.
        """
        self.max_size = max_size
        self.map = OrderedDict()

    def get(self, key, default_value):
        """
        Get a value from the cache by key.
        Args:
            key (any): The key to retrieve the value.
            default_value (Function): The default value to return if the key is not found.

        Returns:
            any: The value associated with the key, or the default value if the key is not found.
        """
        return self.map.get(key, default_value())

    def put(self, key, value):
        """
        Put a key-value pair into the cache.
        Args:
            key (any): The key to store the value.
            value (any): The value to store.
        """
        if len(self.map) >= self.max_size:
            oldest_key = next(iter(self.map))
            self.map.pop(oldest_key)
        self.map[key] = value
