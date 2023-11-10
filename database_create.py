import sqlite3

def create_database():
    conn = sqlite3.connect('cooksoo_cafe.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS couriers (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL
                   )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS categories (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL
                   )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS dishes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   price REAL NOT NULL,
                   category_id INTEGER,
                   FOREIGN KEY (category_id) REFERENCES categories (id)
                   )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS promocodes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   code TEXT NOT NULL,
                   discount REAL NOT NULL
                   )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
