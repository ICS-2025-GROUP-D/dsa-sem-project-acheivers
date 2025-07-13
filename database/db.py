import sqlite3
from typing import Dict, Optional

class InventoryDB:
    def __init__(self, db_path="inventory.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        """Initialize the products table."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                sku TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                stock INTEGER NOT NULL,
                price REAL,
                category TEXT
            )
        """)
        self.conn.commit()

    # CRUD Operations
    def add_product(self, sku: str, name: str, stock: int, price: float, category: str) -> bool:
        """Insert a product into the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO products (sku, name, stock, price, category)
                VALUES (?, ?, ?, ?, ?)
            """, (sku, name, stock, price, category))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # SKU already exists

    def get_product(self, sku: str) -> Optional[Dict]:
        """Fetch a product by SKU."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
        row = cursor.fetchone()
        if row:
            return {"sku": row[0], "name": row[1], "stock": row[2], "price": row[3], "category": row[4]}
        return None

    def get_all_products(self) -> list[dict]:
        """Fetch all products from database for initialization."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM products")
        columns = [column[0] for column in cursor.description]  # Get column names
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_low_stock_products(self, threshold: int = 5) -> list[dict]:
        """Fetch products with stock < threshold for the MinHeap."""
        cursor = self.conn.execute(
            "SELECT sku, stock FROM products WHERE stock < ? ORDER BY stock",
            (threshold,)
        )
        return [dict(row) for row in cursor.fetchall()]

    def add_order(self, sku: str, quantity: int) -> bool:
        """Log orders in the database. Returns `True` if successful."""
        try:
            self.conn.execute(
                "INSERT INTO orders (sku, quantity) VALUES (?, ?)",
                (sku, quantity)
            )
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False  # SKU doesn’t exist or DB went on strike.

    def add_restock_task(self, sku: str, quantity: int) -> bool:
        """Log restock tasks in the database. Returns `True` if successful."""
        try:
            self.conn.execute(
                "INSERT INTO restocks (sku, quantity) VALUES (?, ?)",
                (sku, quantity)
            )
            self.conn.commit()
            return True
        except sqlite3.Error:
            return False  # SKU invalid or DB rebellion.

    def fetch_pending_restocks(self) -> list[dict]:
        """Get all pending restocks for LinkedList initialization."""
        cursor = self.conn.execute("SELECT sku, quantity FROM restocks WHERE is_completed = 0")
        return [dict(row) for row in cursor.fetchall()]

    def log_relationship(self, sku1: str, sku2: str):
        """Log product relationships in the graph."""
        cursor = self.conn.cursor()
        # Upsert: Update frequency if exists, else insert
        cursor.execute("""
            INSERT INTO product_relationships (sku1, sku2, frequency)
            VALUES (?, ?, 1)
            ON CONFLICT(sku1, sku2) DO UPDATE SET frequency = frequency + 1
        """, (sku1, sku2))
        self.conn.commit()

    def get_relationships(self, sku: str) -> list[str]:
        """Fetch related products for the graph."""
        cursor = self.conn.execute("""
            SELECT sku2 FROM product_relationships WHERE sku1 = ?
            UNION
            SELECT sku1 FROM product_relationships WHERE sku2 = ?
        """, (sku, sku))
        return [row[0] for row in cursor.fetchall()]