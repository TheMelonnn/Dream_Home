import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        last_updated TIMESTAMP
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        product_url TEXT NOT NULL,
        image_url TEXT NOT NULL,
        room_id INTEGER NOT NULL,
        quantity INTEGER DEFAULT 1,
        type TEXT NOT NULL,
        FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE CASCADE
    )
''')    

conn.commit()
conn.close()