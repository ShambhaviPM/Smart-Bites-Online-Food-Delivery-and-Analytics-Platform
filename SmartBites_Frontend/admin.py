from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import get_connection

app = Flask(__name__)
app.secret_key = "admin_secret123"

# -------------------- ADMIN LOGIN --------------------
@app.route('/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Only one valid admin
        if username == 'shambhavi' and password == '123@':
            flash("Welcome Admin!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Access Denied ❌", "danger")

    return render_template('admin_login.html')


# -------------------- DASHBOARD --------------------
@app.route('/dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')


# -------------------- DELETE DELIVERY PARTNER --------------------
@app.route('/delete_partner', methods=['GET', 'POST'])
def delete_partner():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        partner_id = request.form['partner_id']
        try:
            # Set related orders to NULL before deletion
            cursor.execute("UPDATE Orders SET partner_id = NULL WHERE partner_id = %s", (partner_id,))
            conn.commit()

            cursor.execute("DELETE FROM DeliveryPartner WHERE partner_id = %s", (partner_id,))
            conn.commit()
            flash("Delivery Partner deleted successfully ✅", "success")
        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    cursor.close()
    conn.close()
    return render_template('delete_partner.html')


# -------------------- VIEW ORDER ITEMS --------------------
@app.route('/view_orderitems')
def view_orderitems():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT oi.orderitem_id, oi.order_id, m.item_name, oi.quantity, oi.subtotal
        FROM OrderItem oi
        JOIN MenuItem m ON oi.item_id = m.item_id
    """)
    orderitems = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_orderitems.html', orderitems=orderitems)


# -------------------- ADD MENU ITEM --------------------
@app.route('/add_menu', methods=['GET', 'POST'])
def add_menu():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT restaurant_id, rest_name FROM Restaurant")
    restaurants = cursor.fetchall()

    if request.method == 'POST':
        restaurant_id = request.form['restaurant_id']
        item_name = request.form['item_name']
        cuisine = request.form['cuisine']
        price = request.form['price']

        cursor.execute("""
            INSERT INTO MenuItem (restaurant_id, item_name, cuisine, price)
            VALUES (%s, %s, %s, %s)
        """, (restaurant_id, item_name, cuisine, price))
        conn.commit()

        flash("Menu item added successfully 🍔", "success")

    cursor.close()
    conn.close()
    return render_template('add_menu.html', restaurants=restaurants)


# -------------------- LOGOUT --------------------
@app.route('/logout')
def logout():
    flash("Logged out successfully.", "info")
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(debug=True)
