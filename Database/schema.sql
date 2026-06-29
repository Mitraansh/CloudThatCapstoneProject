-- Flower Shop database schema

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS flowers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    stock INTEGER NOT NULL CHECK(stock >= 0),
    description TEXT,
    season TEXT,
    FOREIGN KEY(category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS care_instructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flower_id INTEGER NOT NULL,
    topic TEXT NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY(flower_id) REFERENCES flowers(id)
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    flower_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    total_price REAL NOT NULL CHECK(total_price >= 0),
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(flower_id) REFERENCES flowers(id)
);

CREATE TABLE IF NOT EXISTS promotions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    description TEXT,
    discount_percent INTEGER NOT NULL CHECK(discount_percent >= 0 AND discount_percent <= 100),
    active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS support_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
