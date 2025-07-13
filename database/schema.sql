BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS products (
    sku TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    stock INTEGER NOT NULL,
    price REAL,
    category TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    order_date TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (sku) REFERENCES products(sku)
);

CREATE TABLE IF NOT EXISTS restocks (
    sku TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    is_completed BOOLEAN DEFAULT 0,
    FOREIGN KEY (sku) REFERENCES products(sku)
);

CREATE TABLE IF NOT EXISTS product_relationships (
    sku1 TEXT NOT NULL,
    sku2 TEXT NOT NULL,
    frequency INTEGER DEFAULT 1,
    FOREIGN KEY (sku1) REFERENCES products(sku),
    FOREIGN KEY (sku2) REFERENCES products(sku),
    PRIMARY KEY (sku1, sku2)
);

COMMIT;