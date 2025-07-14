class RestockNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class RestockLinkedList:

    def __init__(self):
        self.head = None

    def log_restock(self, restock_entry):
        new_node = RestockNode(restock_entry)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get_all_logs(self):
        logs = []
        current = self.head
        while current:
            logs.append(current.data)
            current = current.next
        return logs

    def clear_logs(self):

        self.head = None
