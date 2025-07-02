class OrderQueue:

    def __init__(self):
        self.orders = []

    def add_order(self, order):
        # order: dict with at least 'sku' and 'quantity'
        self.orders.append(order)

    def next_order(self):
        return self.orders.pop(0) if self.orders else None

    def peek_order(self):
        return self.orders[0] if self.orders else None

    def pending_count(self):
        return len(self.orders)

    def is_empty(self):
        return not self.orders
