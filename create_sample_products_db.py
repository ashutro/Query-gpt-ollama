import sqlite3
from datetime import datetime, timedelta
import random

# Connect to SQLite database (will create if it doesn't exist)
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Drop table if it exists (optional for reruns)
cursor.execute("DROP TABLE IF EXISTS products")

# Create the products table
cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        added_date TEXT NOT NULL
    )
""")

# Sample product names
product_names = [
    "Smartphone", "Laptop", "Headphones", "Monitor", "Keyboard",
    "Mouse", "Tablet", "Camera", "Smartwatch", "Charger"
]

# Generate and insert 20 sample rows
for i in range(20):
    name = random.choice(product_names) + f" {i+1}"
    price = round(random.uniform(50, 1500), 2)
    added_days_ago = random.randint(0, 30)
    added_date = (datetime.now() - timedelta(days=added_days_ago)).strftime('%Y-%m-%d')
    
    cursor.execute("""
        INSERT INTO products (name, price, added_date)
        VALUES (?, ?, ?)
    """, (name, price, added_date))

conn.commit()
conn.close()

print("Sample product data created in 'products.db'")