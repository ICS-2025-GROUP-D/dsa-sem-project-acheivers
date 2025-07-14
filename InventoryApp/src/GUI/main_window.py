import tkinter as tk
from tkinter import ttk

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="yellow")

        self.style_widgets()
        self.create_form()
        self.create_table()
        self.create_log_panel()

    def style_widgets(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        font=("Arial", 10),
                        rowheight=25,
                        background="white",
                        foreground="black",
                        fieldbackground="white")
        style.configure("Treeview.Heading",
                        font=("Arial", 11, "bold"),
                        background="#FFD700",
                        foreground="black")
        style.map('Treeview', background=[('selected', '#FFE87C')])

    def create_form(self):
        form_frame = tk.LabelFrame(self.root, text="Add New Item", bg="white", fg="black", font=("Helvetica", 12, "bold"))
        form_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(form_frame, text="Name:", bg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = tk.Entry(form_frame, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Quantity:", bg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.quantity_entry = tk.Entry(form_frame, font=("Arial", 10))
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Price:", bg="white", font=("Arial", 10)).grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.price_entry = tk.Entry(form_frame, font=("Arial", 10))
        self.price_entry.grid(row=0, column=5, padx=5, pady=5)

        add_button = tk.Button(form_frame, text="Add Item 🛒", command=self.add_item, bg="#FFD700", fg="black", font=("Arial", 10, "bold"))
        add_button.grid(row=0, column=6, padx=10, pady=5)

        update_button = tk.Button(form_frame, text="Update Item 📜", command=self.update_item,
                                  bg="#FFD700", fg="black", font=("Arial", 10, "bold"))
        update_button.grid(row=0, column=7, padx=10, pady=5)

        clear_button = tk.Button(form_frame, text="Clear Form 📝", command=self.clear_form,
                                 bg="#FFD700", fg="black", font=("Arial", 10, "bold"))
        clear_button.grid(row=0, column=8, padx=10, pady=5)

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.log("Form cleared ✅.")

    def create_table(self):
        table_frame = tk.Frame(self.root, bg="white")
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Name", "Quantity", "Price")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.load_item_into_form)

        delete_button = tk.Button(self.root, text="Delete Selected", command=self.delete_item,bg="#FFD700", fg="black", font=("Arial", 10, "bold"))
        delete_button.pack(pady=10)

    def load_item_into_form(self, event):
            selected = self.tree.selection()
            if selected:
                item = selected[0]
                values = self.tree.item(item, 'values')
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, values[0])
                self.quantity_entry.delete(0, tk.END)
                self.quantity_entry.insert(0, values[1])
                self.price_entry.delete(0, tk.END)
                self.price_entry.insert(0, values[2])

    def create_log_panel(self):
        log_frame = tk.LabelFrame(self.root, text="Log Panel", bg="white", fg="black", font=("Helvetica", 12, "bold"))
        log_frame.pack(fill="both", padx=10, pady=5)

        self.log_text = tk.Text(log_frame, height=8, bg="#FFF8DC", fg="black", font=("Courier", 10))
        self.log_text.pack(fill="both", padx=5, pady=5)

    def add_item(self, form_frame=None):
        name = self.name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if name and quantity and price:
            self.tree.insert("", "end", values=(name, quantity, price))
            self.log(f"🌻Added item : {name}, Qty: {quantity}, Price: {price}🌻🌻")

            # Clear entries
            self.name_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
        else:
            self.log("❌Error: Please fill in all fields.❌")

    def delete_item(self):
        selected = self.tree.selection()
        if selected:
            for item in selected:
                values = self.tree.item(item, 'values')
                self.log(f"🗑️ Deleted item: {values}")
                self.tree.delete(item)
        else:
            self.log("❌Error:❌ No item selected to delete.❌")

    def update_item(self):
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            name = self.name_entry.get()
            quantity = self.quantity_entry.get()
            price = self.price_entry.get()

            if name and quantity and price:
                self.tree.item(item, values=(name, quantity, price))
                self.log(f"📝 Updated item: {name}, Qty: {quantity}, Price: {price}")

                # Clear form
                self.clear_form()
            else:
                self.log("Error: Please fill in all fields.")
        else:
            self.log("Error: No item selected to update.")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
