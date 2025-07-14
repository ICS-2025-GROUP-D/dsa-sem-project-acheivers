import tkinter as tk
from tkinter import ttk


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")

        self.create_form()
        self.create_table()
        self.create_log_panel()

    def create_form(self):
        form_frame = tk.LabelFrame(self.root, text="Add New Item")
        form_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5)
        self.quantity_entry = tk.Entry(form_frame)
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Price:").grid(row=0, column=4, padx=5, pady=5)
        self.price_entry = tk.Entry(form_frame)
        self.price_entry.grid(row=0, column=5, padx=5, pady=5)

        add_button = tk.Button(form_frame, text="Add Item", command=self.add_item)
        add_button.grid(row=0, column=6, padx=5, pady=5)

    def create_table(self):
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Name", "Quantity", "Price")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)

        delete_button = tk.Button(self.root, text="Delete Selected", command=self.delete_item)
        delete_button.pack(pady=5)

    def create_log_panel(self):
        log_frame = tk.LabelFrame(self.root, text="Log Panel")
        log_frame.pack(fill="both", padx=10, pady=5)

        self.log_text = tk.Text(log_frame, height=8)
        self.log_text.pack(fill="both")

    def add_item(self):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if name and quantity and price:
            self.tree.insert("", "end", values=(name, quantity, price))
            self.log(f"Added item: {name}, Qty: {quantity}, Price: {price}")

            # Clear entries
            self.name_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
        else:
            self.log("Error: Please fill in all fields.")

    def delete_item(self):
        selected = self.tree.selection()
        if selected:
            for item in selected:
                values = self.tree.item(item, 'values')
                self.log(f"Deleted item: {values}")
                self.tree.delete(item)
        else:
            self.log("Error: No item selected to delete.")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
