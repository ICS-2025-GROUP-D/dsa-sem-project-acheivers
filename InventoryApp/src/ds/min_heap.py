import heapq

class LowStockMinHeap:

    def __init__(self):
        self.heap = []

    def add_product(self, product):

        if 'sku' in product and 'quantity' in product:
            heapq.heappush(self.heap, (product['quantity'], product['sku'], product))

    def get_lowest_stock(self, count=3):
        return [item[2] for item in heapq.nsmallest(count, self.heap)]

    def remove_lowest(self):
        return heapq.heappop(self.heap)[2] if self.heap else None

    def is_empty(self):
        return len(self.heap) == 0
