from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import qrcode
from io import BytesIO
import base64
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

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
    """
    Adds a new dish to the database.
    ---
    tags:
      - Dish Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Name of the dish
      - name: price
        in: formData
        type: number
        required: true
        description: Price of the dish
      - name: image_link
        in: formData
        type: string
        required: false
        description: URL link to the image of the dish
      - name: category_id
        in: formData
        type: integer
        required: true
        description: ID of the category the dish belongs to
      - name: sub_category_id
        in: formData
        type: integer
        required: false
        description: ID of the sub-category the dish belongs to
    responses:
      200:
        description: Dish successfully added
    """
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
    """
    Edits an existing dish in the database.
    ---
    tags:
      - Dish Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: dish_id
        in: path
        type: integer
        required: true
        description: Unique ID of the dish
      - name: name
        in: formData
        type: string
        required: true
        description: Updated name of the dish
      - name: price
        in: formData
        type: number
        required: true
        description: Updated price of the dish
      - name: category_id
        in: formData
        type: integer
        required: true
        description: Updated ID of the category the dish belongs to
      - name: sub_category_id
        in: formData
        type: integer
        required: false
        description: Updated ID of the sub-category the dish belongs to
    responses:
      200:
        description: Dish successfully updated
      404:
        description: Dish not found
    """
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
    """
    Deletes an existing dish from the database.
    ---
    tags:
      - Dish Management
    parameters:
      - name: dish_id
        in: path
        type: integer
        required: true
        description: Unique ID of the dish to delete
    responses:
      200:
        description: Dish successfully deleted
      404:
        description: Dish not found
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM dishes WHERE id = ?', (dish_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('menu'))

# --- Category Management ---

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    """
    Adds a new category to the database.
    ---
    tags:
      - Category Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Name of the category to add
    responses:
      200:
        description: Category successfully added
      400:
        description: Error with the provided data
    """
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
    """
    Edits an existing category in the database.
    ---
    tags:
      - Category Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
        description: Unique ID of the category to edit
      - name: name
        in: formData
        type: string
        required: true
        description: Updated name of the category
    responses:
      200:
        description: Category successfully updated
      404:
        description: Category not found
    """
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        conn.execute('UPDATE categories SET name = ? WHERE id = ?', (name, category_id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    category = conn.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
    conn.close()
    if category is None:
        abort(404)  # Category not found
    return render_template('edit_category.html', category=category)

@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    """
    Deletes an existing category from the database.
    ---
    tags:
      - Category Management
    parameters:
      - name: category_id
        in: path
        type: integer
        required: true
        description: Unique ID of the category to delete
    responses:
      200:
        description: Category successfully deleted
      404:
        description: Category not found
    """
    conn = get_db_connection()
    conn.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/add_sub_category', methods=['GET', 'POST'])
def add_sub_category():
    """
    Adds a new sub-category to the database.
    ---
    tags:
      - Sub-Category Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Name of the sub-category to add
      - name: category_id
        in: formData
        type: integer
        required: true
        description: ID of the parent category
    responses:
      200:
        description: Sub-category successfully added
      400:
        description: Error with the provided data
    """
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
    """
    Edits an existing sub-category in the database.
    ---
    tags:
      - Sub-Category Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: sub_category_id
        in: path
        type: integer
        required: true
        description: Unique ID of the sub-category to edit
      - name: name
        in: formData
        type: string
        required: true
        description: Updated name of the sub-category
      - name: category_id
        in: formData
        type: integer
        required: true
        description: Updated ID of the parent category
    responses:
      200:
        description: Sub-category successfully updated
      404:
        description: Sub-category not found
    """
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
    """
    Deletes an existing sub-category from the database.
    ---
    tags:
      - Sub-Category Management
    parameters:
      - name: sub_category_id
        in: path
        type: integer
        required: true
        description: Unique ID of the sub-category to delete
    responses:
      200:
        description: Sub-category successfully deleted
      404:
        description: Sub-category not found
    """
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
    """
    Adds a new courier to the database.
    ---
    tags:
      - Courier Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: name
        in: formData
        type: string
        required: true
        description: Full name of the courier
    responses:
      200:
        description: Courier successfully added
      400:
        description: Error with the provided data
    """ 
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
    """
    Edits an existing courier's information.
    ---
    tags:
      - Courier Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: courier_id
        in: path
        type: integer
        required: true
        description: The unique identifier for the courier
      - name: name
        in: formData
        type: string
        required: true
        description: The updated full name of the courier
    responses:
      200:
        description: Courier information successfully updated
      404:
        description: Courier not found
    """
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
    """
    Deletes a courier from the database.
    ---
    tags:
      - Courier Management
    parameters:
      - name: courier_id
        in: path
        type: integer
        required: true
        description: The unique identifier for the courier to delete
    responses:
      200:
        description: Courier successfully deleted
      404:
        description: Courier not found
    """
    # Delete courier logic
    conn = get_db_connection()
    conn.execute('DELETE FROM couriers WHERE id = ?', (courier_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/couriers')
def couriers():
    """
    Retrieves a list of all couriers.
    ---
    tags:
      - Courier Management
    responses:
      200:
        description: A list of couriers
      500:
        description: Error retrieving couriers
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE role = 'courier'")
    couriers = cur.fetchall()
    conn.close()
    return render_template('couriers.html', couriers=couriers)

# --- Order Management ---
@app.route('/orders')
def orders():
    """
    Retrieves a list of all orders.
    ---
    tags:
      - Order Management
    responses:
      200:
        description: A list of orders
      500:
        description: Error retrieving orders
    """
    # Display orders
    conn = get_db_connection()
    cur.execute('''Select * from orders''')
    orders = cur.fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/send_order_to_kitchen/<int:order_id>', methods=['POST'])
def send_order_to_kitchen(order_id):
    """
    Updates the status of an order to 'In Kitchen'.
    ---
    tags:
      - Order Management
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: The unique identifier for the order
    responses:
      200:
        description: Order status updated to 'In Kitchen'
      404:
        description: Order not found
    """
    # Send order to kitchen logic
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', ('In Kitchen', order_id))
    conn.commit()
    conn.close()
    return redirect(url_for('orders'))

@app.route('/order_details/<int:order_id>')
def order_details(order_id):
    """
    Retrieves details for a specific order.
    ---
    tags:
      - Order Management
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: The unique identifier for the order
    responses:
      200:
        description: Details of the specified order
      404:
        description: Order not found
    """
    # View detailed information about the order
    conn = get_db_connection()
    cur.execute('''Select * from orders where id = ?''', (order_id,))
    order = cur.fetchall()
    conn.close()
    return render_template('order_details.html', order_id=order_id)

# --- Branch Management ---
@app.route('/add_branch', methods=['GET', 'POST'])
def add_branch():
    """
    Adds a new branch location.
    ---
    tags:
      - Branch Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: branch_name
        in: formData
        type: string
        required: true
        description: Name of the branch
      - name: address
        in: formData
        type: string
        required: true
        description: Address of the branch
      - name: phone
        in: formData
        type: string
        required: true
        description: Contact phone number for the branch
    responses:
      200:
        description: Branch successfully added
      400:
        description: Error with the provided data
    """
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
    """
    Edits an existing branch location's information.
    ---
    tags:
      - Branch Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: branch_id
        in: path
        type: integer
        required: true
        description: The unique identifier for the branch
      - name: branch_name
        in: formData
        type: string
        required: true
        description: Updated name of the branch
      - name: address
        in: formData
        type: string
        required: true
        description: Updated address of the branch
      - name: phone
        in: formData
        type: string
        required: true
        description: Updated contact phone number for the branch
    responses:
      200:
        description: Branch information successfully updated
      404:
        description: Branch not found
    """
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
    """
    Deletes a branch location from the database.
    ---
    tags:
      - Branch Management
    parameters:
      - name: branch_id
        in: path
        type: integer
        required: true
        description: The unique identifier for the branch to delete
    responses:
      200:
        description: Branch successfully deleted
      404:
        description: Branch not found
    """
    # Logic to delete a branch
    conn = get_db_connection()
    conn.execute('DELETE FROM branch WHERE id = ?', (branch_id,))
    conn.commit()
    conn.close()
    return render_template('admin_panel.html')

@app.route('/branches')
def branches():
    """
    Retrieves a list of all branch locations.
    ---
    tags:
      - Branch Management
    responses:
      200:
        description: A list of branches
      500:
        description: Error retrieving branches
    """
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
    """
    Adds a new promo code to the database.
    ---
    tags:
      - Promo Code Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: code
        in: formData
        type: string
        required: true
        description: The promo code
      - name: discount
        in: formData
        type: number
        required: true
        description: The discount percentage for the promo code
    responses:
      200:
        description: Promo code successfully added
      400:
        description: Error with the provided data
    """
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
    """
    Deletes an existing promo code from the database.
    ---
    tags:
      - Promo Code Management
    parameters:
      - name: promo_id
        in: path
        type: integer
        required: true
        description: The unique identifier for the promo code
    responses:
      200:
        description: Promo code successfully deleted
      404:
        description: Promo code not found
    """
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
    """
    Retrieves the menu items, optionally filtered by category.
    ---
    tags:
      - Menu Management
    parameters:
      - name: category_id
        in: formData
        type: integer
        required: false
        description: Optional category ID to filter the menu items
    responses:
      200:
        description: A list of menu items, optionally filtered by category
      500:
        description: Error retrieving menu items
    """
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

@app.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    """
    Updates the status of a specific order.
    ---
    tags:
      - Order Management
    consumes:
      - application/x-www-form-urlencoded
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: The unique identifier for the order
      - name: status
        in: formData
        type: string
        required: true
        enum: ['Pending', 'In Kitchen', 'Ready for Pickup', 'Completed']
        description: The new status for the order
    responses:
      200:
        description: Order status successfully updated
      404:
        description: Order not found
    """
    status = request.form.get('status')
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the order exists
    cur.execute('SELECT id FROM orders WHERE id = ?', (order_id,))
    if cur.fetchone() is None:
        conn.close()
        abort(404)  # Not found

    # Update the order status
    cur.execute('UPDATE orders SET status = ? WHERE id = ?', (status, order_id))
    conn.commit()
    conn.close()

    return redirect(url_for('orders'))


if __name__ == '__main__':
    app.run(debug=True)