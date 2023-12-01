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

# --- Dish Management ---
@app.route('/add_dish', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category_id = request.form['category_id']
        conn = get_db_connection()
        conn.execute('INSERT INTO dishes (name, price, category_id, sub_category_id) VALUES (?, ?, ?, ?)', (name, price, category_id, sub_category_id))
        categories = conn.execute('SELECT * FROM categories').fetchall()
        sub_category = conn.execute('SELECT * FROM sub_category').fetchall()
        conn.commit()
        conn.close()
        return render_template('add_dish.html', categories=categories, sub_category=sub_category)
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('add_dish.html', categories=categories)
    
@app.route('/edit_dish/<int:dish_id>', methods=['GET', 'POST'])
def edit_dish(dish_id):
    if request.method == 'POST':
        # Logic to edit a dish
        conn = get_db_connection()
        conn.execute('UPDATE dishes SET name = ?, price = ?, category_id = ? WHERE id = ?', (name, price, category_id, dish_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    return render_template('edit_dish.html', dish_id=dish_id)

@app.route('/delete_dish/<int:dish_id>', methods=['POST'])
def delete_dish(dish_id):
    # Logic to delete a dish
    conn = get_db_connection()
    conn.execute('DELETE FROM dishes WHERE id = ?', (dish_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

# --- Category Management ---

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
    # Display a list of couriers
    conn = get_db_connection()
    cur.execute('''Select * from users where role = 'courier''')
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
        # Logic to add a branch
        return redirect(url_for('admin_panel'))
    return render_template('add_branch.html')

@app.route('/edit_branch/<int:branch_id>', methods=['GET', 'POST'])
def edit_branch(branch_id):
    if request.method == 'POST':
        # Logic to edit a branch
        return redirect(url_for('admin_panel'))
    # Fetch branch details to populate the form
    return render_template('edit_branch.html', branch_id=branch_id)

@app.route('/delete_branch/<int:branch_id>', methods=['POST'])
def delete_branch(branch_id):
    # Logic to delete a branch
    conn = get_db_connection()
    conn.execute('DELETE FROM branch WHERE id = ?', (branch_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/branches')
def branches():
    # Logic to display a list of branches
    conn = get_db_connection()
    cur.execute('''Select * from branch''')
    branches = cur.fetchall()
    conn.close()
    return render_template('branches.html', branches=branches)

# --- Promo Code Management ---
@app.route('/add_promocode', methods=['GET', 'POST'])
def add_promocode():
    if request.method == 'POST':
        code = request.form['code']
        discount = request.form['discount']
        conn = get_db_connection()
        conn.execute('INSERT INTO promocodes (code, discount) VALUS (?, ?)', (code, discount))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    return render_template('add_promocode.html')

@app.route('/delete_promocode/<int:promo_id>', methods=['POST'])
def delete_promocode(promo_id):
    # Delete promo code logic
    conn = get_db_connection()
    conn.execute('DELETE FROM promocodes WHERE id = ?', (promo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

# --- Additional Features ---
# Implement routes and logic for any additional features required

if __name__ == '__main__':
    app.run(debug=True)