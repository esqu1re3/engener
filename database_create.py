import sqlite3

def create_database():
    conn = sqlite3.connect('cooksoo_cafe.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS user (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   phone TEXT NOT NULL,
                   role TEXT NOT NULL
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
                   img_link TEXT,
                   FOREIGN KEY (category_id) REFERENCES categories (id)
                   )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS promocodes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   code TEXT NOT NULL,
                   discount REAL NOT NULL
                   )''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS orders (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   description TEXT,
                   status TEXT,
                   Foreign Key (courier_id) REFERENCES couriers (id),
                     Foreign Key (dish_id) REFERENCES dishes (id),
                   )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS branch ()
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    phone TEXT NOT NULL,
                     ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS sub_category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                    )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
