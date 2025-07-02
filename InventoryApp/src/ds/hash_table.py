class ProductHashTable:
   
    def __init__(self, capacity=101):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    def _hash(self, sku):
        return hash(sku) % self.capacity

    def add_product(self, sku, data):
        index = self._hash(sku)
        bucket = self.table[index]
        for pair in bucket:
            if pair[0] == sku:
                pair[1] = data
                return "Product updated"
        bucket.append([sku, data])
        return "Product added"

    def get_product(self, sku):
        index = self._hash(sku)
        for k, v in self.table[index]:
            if k == sku:
                return v
        return None

    def remove_product(self, sku):
        index = self._hash(sku)
        bucket = self.table[index]
        for i, (k, _) in enumerate(bucket):
            if k == sku:
                del bucket[i]
                return True
        return False

    def list_all_skus(self):
        return [k for bucket in self.table for k, _ in bucket]
