import mysql.connector
from mysql.connector import Error
from typing import Dict, Optional, List


class InventoryDB:
    def __init__(self, host='localhost', database='inventory', user='root', password=''):
        """Initialize MySQL database connection"""
        try:
            self.conn = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            self._create_tables()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def _create_tables(self):
        """Initialize all required tables if they don't exist"""
        cursor = self.conn.cursor()

        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                sku VARCHAR(50) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                stock INT NOT NULL,
                price DECIMAL(10,2),
                category VARCHAR(100)
            )
        """)

        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sku VARCHAR(50),
                quantity INT,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sku) REFERENCES products(sku)
            )
        """)

        # Restocks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS restocks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sku VARCHAR(50),
                quantity INT,
                is_completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sku) REFERENCES products(sku)
            )
        """)

        # Product relationships table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_relationships (
                sku1 VARCHAR(50),
                sku2 VARCHAR(50),
                frequency INT DEFAULT 1,
                PRIMARY KEY (sku1, sku2),
                FOREIGN KEY (sku1) REFERENCES products(sku),
                FOREIGN KEY (sku2) REFERENCES products(sku)
            )
        """)

        self.conn.commit()

    def add_product(self, sku: str, name: str, stock: int, price: float, category: str) -> bool:
        """Insert a product into the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO products (sku, name, stock, price, category)
                VALUES (%s, %s, %s, %s, %s)
            """, (sku, name, stock, price, category))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error adding product: {e}")
            return False

    def get_product(self, sku: str) -> Optional[Dict]:
        """Fetch a product by SKU."""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE sku = %s", (sku,))
        return cursor.fetchone()

    def get_all_products(self) -> List[Dict]:
        """Fetch all products from database for initialization."""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()

    def get_low_stock_products(self, threshold: int = 5) -> List[Dict]:
        """Fetch products with stock < threshold for the MinHeap."""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT sku, stock FROM products WHERE stock < %s ORDER BY stock",
            (threshold,)
        )
        return cursor.fetchall()

    def add_order(self, sku: str, quantity: int) -> bool:
        """Log orders in the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO orders (sku, quantity) VALUES (%s, %s)",
                (sku, quantity)
            )
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error adding order: {e}")
            return False

    def add_restock_task(self, sku: str, quantity: int) -> bool:
        """Log restock tasks in the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO restocks (sku, quantity) VALUES (%s, %s)",
                (sku, quantity)
            )
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error adding restock task: {e}")
            return False

    def fetch_pending_restocks(self) -> List[Dict]:
        """Get all pending restocks for LinkedList initialization."""
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT sku, quantity FROM restocks WHERE is_completed = FALSE")
        return cursor.fetchall()

    def mark_restock_completed(self, sku: str) -> bool:
        """Mark a restock as completed."""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE restocks SET is_completed = TRUE WHERE sku = %s",
                (sku,)
            )
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error completing restock: {e}")
            return False

    def log_relationship(self, sku1: str, sku2: str) -> bool:
        """Log product relationships in the graph."""
        try:
            cursor = self.conn.cursor()
            # Using ON DUPLICATE KEY UPDATE for MySQL
            cursor.execute("""
                INSERT INTO product_relationships (sku1, sku2, frequency)
                VALUES (%s, %s, 1)
                ON DUPLICATE KEY UPDATE frequency = frequency + 1
            """, (sku1, sku2))
            self.conn.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Error logging relationship: {e}")
            return False

    def get_relationships(self, sku: str) -> List[str]:
        """Fetch related products for the graph."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT sku2 FROM product_relationships WHERE sku1 = %s
            UNION
            SELECT sku1 FROM product_relationships WHERE sku2 = %s
        """, (sku, sku))
        return [row[0] for row in cursor.fetchall()]

    def __del__(self):
        """Close the database connection when the object is destroyed"""
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.conn.close()