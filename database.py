import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    invoice TEXT,
    amount INTEGER,
    status TEXT
)
""")
conn.commit()

def create_order(user_id, invoice, amount):
    cursor.execute(
        "INSERT INTO orders (user_id, invoice, amount, status) VALUES (?, ?, ?, ?)",
        (user_id, invoice, amount, "UNPAID")
    )
    conn.commit()

def mark_paid(invoice):
    cursor.execute(
        "UPDATE orders SET status='PAID' WHERE invoice=?",
        (invoice,)
    )
    conn.commit()
