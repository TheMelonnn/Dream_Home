import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
    ALTER TABLE products ADD COLUMN notes TEXT
''') 

conn.commit()
conn.close()