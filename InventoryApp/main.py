# InventoryApp/main.py

from src.ds.hash_table import ProductHashTable
from src.ds.min_heap import LowStockMinHeap
from src.ds.queue import OrderQueue
from src.ds.linked_list import RestockLinkedList
from src.utils.logger import log_event

if __name__ == "__main__":
    log_event("Launching InventoryApp backend module...")


    inventory = ProductHashTable()
    low_stock = LowStockMinHeap()
    orders = OrderQueue()
    restock_logs = RestockLinkedList()


    product = {
        'sku': 'P001',
        'name': 'Milk',
        'quantity': 3,
        'price': 50,
        'total_sold': 25
    }


    log_event(f"Adding product: {product}")
    inventory.add_product(product['sku'], product)
    low_stock.add_product(product)
    restock_logs.log_restock(f"Restocked {product['sku']} with {product['quantity']} units.")


    orders.add_order({'sku': 'P001', 'quantity': 1})


    log_event("Inventory Lookup:")
    print(inventory.get_product('P001'))

    log_event("Low Stock Items:")
    for item in low_stock.get_lowest_stock():
        print(item)

    log_event("Order in Queue:")
    print(orders.peek_order())

    log_event("Restock Logs:")
    for entry in restock_logs.get_all_logs():
        print(entry)
