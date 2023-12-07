from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('cooksoo_cafe.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('admin_panel.html')

# --- Dish Management ---
@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        img_link = request.form['image_link']
        category_id = request.form['category_id']
        sub_category_id = request.form.get('sub_category_id')
        conn.execute('INSERT OR IGNORE INTO dishes (name, price, category_id, sub_category_id, img_link) VALUES (?, ?, ?, ?, ?)', 
                     (name, price, category_id, sub_category_id, img_link))
        conn.commit()
        conn.close()
        return render_template('add_dish.html', message="Dish added successfully")

    categories = conn.execute('SELECT * FROM categories').fetchall()
    sub_categories = conn.execute('SELECT * FROM sub_category').fetchall()
    conn.close()
    return render_template('add_dish.html', categories=categories, sub_categories=sub_categories)

@app.route('/edit_dish/<int:dish_id>', methods=['GET', 'POST'])
def edit_dish(dish_id):
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category_id = request.form['category_id']
        sub_category_id = request.form.get('sub_category_id')
        conn.execute('UPDATE dishes SET name = ?, price = ?, category_id = ?, sub_category_id = ? WHERE id = ?', 
                     (name, price, category_id, sub_category_id, dish_id))
        conn.commit()
        conn.close()
        conn = get_db_connection()
        dish = conn.execute('SELECT * FROM dishes WHERE id = ?', (dish_id,)).fetchone()
        conn.close()
        return render_template('menu.html', dish=dish)

    dish = conn.execute('SELECT * FROM dishes WHERE id = ?', (dish_id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    sub_categories = conn.execute('SELECT * FROM sub_category').fetchall()
    conn.close()
    return render_template('edit_dish.html', dish=dish, categories=categories, sub_categories=sub_categories)

@app.route('/delete_dish/<int:dish_id>', methods=['POST'])
def delete_dish(dish_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM dishes WHERE id = ?', (dish_id,))
    conn.commit()
    conn.close()
    conn = get_db_connection()
    dishes = conn.execute('SELECT * FROM dishes').fetchall()
    conn.close()
    return render_template('menu.html', dishes=dishes)

# --- Category Management ---

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''select * from categories''')
    categories = cur.fetchall()
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db_connection()
        conn.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (name,))
        conn.commit()
        cur = conn.cursor()
        cur.execute('''select * from categories''')
        categories = cur.fetchall()
        conn.close()
        return render_template("add_category.html", categories=categories)
    return render_template('add_category.html', categories=categories)

@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    if request.method == 'POST':
        # Logic to edit a category
        name = request.form['name']
        category_id = request.form['category_id']
        conn = get_db_connection()
        conn.execute('UPDATE categories SET name = ? WHERE id = ?', (name, category_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    # Fetch category details to populate the form
    conn = get_db_connection()
    cur.execute('''Select * from categories where id = ?''', (category_id,))
    category = cur.fetchall()
    conn.close()
    return render_template('edit_category.html', category=category)

@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    # Logic to delete a category
    conn = get_db_connection()
    conn.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/add_sub_category', methods=['GET', 'POST'])
def add_sub_category():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch categories for the dropdown
    cur.execute('SELECT * FROM categories')
    categories = cur.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']

        # Insert the new sub-category
        cur.execute('INSERT OR IGNORE INTO sub_category (name, category_id) VALUES (?, ?)', (name, category_id))
        conn.commit()

    # Fetch sub-categories to display on the page
    cur.execute('SELECT * FROM sub_category')
    sub_categories = cur.fetchall()

    conn.close()

    return render_template('add_sub_category.html', sub_categories=sub_categories, categories=categories)

@app.route('/edit_sub_category/<int:sub_category_id>', methods=['GET', 'POST'])
def edit_sub_category(sub_category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''select * from categories''')
    categories = cur.fetchall()
    if request.method == 'POST':
        # Logic to edit a category
        name = request.form['name']
        category_id = request.form['category_id']
        conn = get_db_connection()
        conn.execute('UPDATE sub_category SET name = ?, category_id = ? WHERE id = ?', (name, category_id, sub_category_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    # Fetch category details to populate the form
    conn = get_db_connection()
    cur.execute('''Select * from sub_category where id = ?''', (sub_category_id,))
    sub_category = cur.fetchall()
    conn.close()
    return render_template('edit_sub_category.html', sub_category=sub_category, categories=categories)

@app.route('/delete_sub_category/<int:sub_category_id>', methods=['POST'])
def delete_sub_category(sub_category_id):
    # Logic to delete a category
    conn = get_db_connection()
    conn.execute('DELETE FROM sub_category WHERE id = ?', (sub_category_id,))
    conn.commit()
    cur = conn.cursor()
    cur.execute('''select * from sub_category''')
    sub_categories = cur.fetchall()
    conn.close()
    return render_template('admin_panel.html')

# --- Courier Management ---
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

@app.route('/edit_courier/<int:courier_id>', methods=['GET', 'POST'])
def edit_courier(courier_id):
    # Edit courier logic
    if request.method == 'POST':
        # Logic to edit a courier
        conn = get_db_connection()
        conn.execute('UPDATE couriers SET name = ? WHERE id = ?', (name, courier_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    return render_template('edit_courier.html', courier_id=courier_id)

@app.route('/delete_courier/<int:courier_id>', methods=['POST'])
def delete_courier(courier_id):
    # Delete courier logic
    conn = get_db_connection()
    conn.execute('DELETE FROM couriers WHERE id = ?', (courier_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/couriers')
def couriers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE role = 'courier'")
    couriers = cur.fetchall()
    conn.close()
    return render_template('couriers.html', couriers=couriers)

# --- Order Management ---
@app.route('/orders')
def orders():
    # Display orders
    conn = get_db_connection()
    cur.execute('''Select * from orders''')
    orders = cur.fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/send_order_to_kitchen/<int:order_id>', methods=['POST'])
def send_order_to_kitchen(order_id):
    # Send order to kitchen logic
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', ('In Kitchen', order_id))
    conn.commit()
    conn.close()
    return redirect(url_for('orders'))

@app.route('/order_details/<int:order_id>')
def order_details(order_id):
    # View detailed information about the order
    conn = get_db_connection()
    cur.execute('''Select * from orders where id = ?''', (order_id,))
    order = cur.fetchall()
    conn.close()
    return render_template('order_details.html', order_id=order_id)

# --- Branch Management ---
@app.route('/add_branch', methods=['GET', 'POST'])
def add_branch():
    if request.method == 'POST':
        branch_name = request.form['branch_name']
        address = request.form['address']
        phone = request.form['phone']  # Get phone number from the form

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO branch (name, address, phone) VALUES (?, ?, ?)', (branch_name, address, phone))
        conn.commit()
        conn.close()

        return render_template('add_branch.html', message="Branch added successfully")

    return render_template('add_branch.html')

@app.route('/edit_branch/<int:branch_id>', methods=['GET', 'POST'])
def edit_branch(branch_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        branch_name = request.form['branch_name']
        address = request.form['address']
        phone = request.form['phone']

        cur.execute('UPDATE branch SET name = ?, address = ?, phone = ? WHERE id = ?', 
                    (branch_name, address, phone, branch_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))

    # Fetch branch details for GET request
    cur.execute('SELECT name, address, phone FROM branch WHERE id = ?', (branch_id,))
    branch = cur.fetchone()
    conn.close()

    if branch is None:
        abort(404)  # Branch not found

    return render_template('edit_branch.html', branch=branch, branch_id=branch_id)


@app.route('/delete_branch/<int:branch_id>', methods=['POST'])
def delete_branch(branch_id):
    # Logic to delete a branch
    conn = get_db_connection()
    conn.execute('DELETE FROM branch WHERE id = ?', (branch_id,))
    conn.commit()
    conn.close()
    return render_template('admin_panel.html')

@app.route('/branches')
def branches():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM branch")
    branches = cur.fetchall()
    conn.close()
    return render_template('branches.html', branches=branches)

# --- Promo Code Management ---
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return buffered.getvalue()

@app.route('/add_promocode', methods=['GET', 'POST'])
def add_promocode():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        code = request.form['code']
        discount = request.form['discount']
        qr_code_blob = generate_qr_code(code)

        cur.execute('INSERT INTO promocodes (code, discount, qr_code) VALUES (?, ?, ?)', 
                    (code, discount, qr_code_blob))
        conn.commit()

    cur.execute('SELECT code, discount, qr_code FROM promocodes')
    promocodes = []
    for row in cur.fetchall():
        code, discount, qr_blob = row
        qr_base64 = base64.b64encode(qr_blob).decode()
        promocodes.append((code, discount, qr_base64))

    conn.close()
    return render_template('add_promocode.html', promocodes=promocodes)

@app.route('/delete_promocode/<int:promo_id>', methods=['POST'])
def delete_promocode(promo_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the promocode exists
    cur.execute('SELECT id FROM promocodes WHERE id = ?', (promo_id,))
    if cur.fetchone() is None:
        conn.close()
        abort(404)  # Not found

    # Delete the promocode
    cur.execute('DELETE FROM promocodes WHERE id = ?', (promo_id,))
    conn.commit()
    conn.close()

    return render_template('admin_panel.html')

# --- Additional Features ---
# Implement routes and logic for any additional features required

def get_dishes():
    conn = sqlite3.connect('cooksoo_cafe.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM dishes")
    dishes = cur.fetchall()
    conn.close()
    return dishes

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    conn = get_db_connection()
    cur = conn.cursor()

    selected_category_id = request.form.get('category_id') if request.method == 'POST' else None

    # Fetch categories for the filter dropdown
    cur.execute('SELECT * FROM categories')
    categories = cur.fetchall()

    # Fetch dishes, filtered by category if selected
    query = 'SELECT * FROM dishes'
    if selected_category_id:
        query += ' WHERE category_id = ?'
        cur.execute(query, (selected_category_id,))
    else:
        cur.execute(query)
    dishes = cur.fetchall()

    conn.close()
    return render_template('menu.html', categories=categories, dishes=dishes, selected_category_id=selected_category_id)


if __name__ == '__main__':
    app.run(debug=True)