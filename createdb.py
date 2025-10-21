import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')
conn.commit()
conn.close()