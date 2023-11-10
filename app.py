from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cooksoo_cafe.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('admin_panel.html')

@app.route('/add_courier', methods=['GET', 'POST'])
def add_courier():
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        conn.execute('INSERT INTO couriers (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    return render_template('add_courier.html')

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        conn.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    return render_template('add_category.html')

@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category_id = request.form['category_id']
        conn = get_db_connection()
        conn.execute('INSERT INTO dishes (name, price, category_id) VALUES (?, ?, ?)', (name, price, category_id))
        categories = conn.execute('SELECT * FROM categories').fetchall()
        conn.commit()
        conn.close()
        return render_template('add_dish.html', categories=categories)
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('add_dish.html', categories=categories)

@app.route('/add_promocode', methods=['GET', 'POST'])
def add_promocode():
    if request.method == 'POST':
        code = request.form['code']
        discount = request.form['discount']
        conn = get_db_connection()
        conn.execute('INSERT INTO promocodes (code, discount) VALUES (?, ?)', (code, discount))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    return render_template('add_promocode.html')

@app.route('/menu')
def menu():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    menu = {}
    for category in categories:
        dishes = conn.execute('SELECT * FROM dishes WHERE category_id = ?', (category['id'],)).fetchall()
        menu[category['name']] = dishes
    conn.close()
    return render_template('menu.html', menu=menu)

@app.route('/admin')
def admin_panel():
    return render_template('admin_panel.html')

if __name__ == '__main__':
    app.run(debug=True)
