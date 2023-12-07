import sqlite3

def create_database():
    conn = sqlite3.connect('cooksoo_cafe.db')
    cur = conn.cursor()

    # Define the user table with role
    cur.execute('''CREATE TABLE IF NOT EXISTS user (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   phone TEXT NOT NULL,
                   role TEXT CHECK(role IN ('kitchen', 'administration', 'courier')) NOT NULL
                   )''')

    # Define other tables
    cur.execute('''CREATE TABLE IF NOT EXISTS categories (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL
                   )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS dishes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   price REAL NOT NULL,
                   category_id INTEGER,
                   sub_category_id INTEGER, 
                   img_link TEXT,
                   FOREIGN KEY (category_id) REFERENCES categories (id),
                   FOREIGN KEY (sub_category_id) REFERENCES sub_category (id)
                   )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS promocodes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   code TEXT NOT NULL,
                   discount REAL NOT NULL,
                   qr_code BLOB
                   )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS orders (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   description TEXT,
                   status TEXT,
                   user_id INTEGER,
                   dish_id INTEGER,
                   FOREIGN KEY (user_id) REFERENCES user (id),
                   FOREIGN KEY (dish_id) REFERENCES dishes (id)
                   )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS branch (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    phone TEXT NOT NULL
                     )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS sub_category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories (id)
                    )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()