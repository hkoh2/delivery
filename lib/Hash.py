# Hash.py

class ChainingHashTable:
    def __init__(self, capacity=10):
        # Initialize buckets with lists
        self.buckets = [[] for _ in range(capacity)]

    '''
    Inserts a new value into the chaining hash table.
    '''
    def insert(self, key, val):
        # Find the bucket for the key provided
        bucket_key = hash(key) % len(self.buckets)
        bucket_list = self.buckets[bucket_key]

        # Value is updated if the key exists
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = val
                return True

        # If key is not found, add as a new element in the bucket
        bucket_list.append([key, val])
        return True

    '''
    Search for value by key. Returns value if key exists. None if does not exist.
    '''
    def search(self, key):
        # Find the bucket for the key provided
        bucket_key = hash(key) % len(self.buckets)
        bucket_list = self.buckets[bucket_key]

        # search for the key in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    '''
    Remove key and value if key exists in the hash table'''
    def remove(self, key):
        # Find the bucket for the key provided
        bucket_key = hash(key) % len(self.buckets)
        bucket_list = self.buckets[bucket_key]

        # Remove key value if it exists
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
