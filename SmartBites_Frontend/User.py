from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

# -------------------- REGISTER --------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        street = request.form['street']
        city = request.form['city']
        pin = request.form['pin']
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Customer (customer_name, customer_email, customer_phno, customer_street, customer_city, customer_pin)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, email, phone, street, city, pin))
        conn.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        customer_id = cursor.fetchone()[0]

        password_hash = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO UserAuth (customer_id, username, password_hash)
            VALUES (%s, %s, %s)
        """, (customer_id, username, password_hash))
        conn.commit()

        cursor.close()
        conn.close()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# -------------------- LOGIN --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM UserAuth WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[0], password):
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password", "danger")

        cursor.close()
        conn.close()
    return render_template('login.html')


# -------------------- DASHBOARD --------------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# -------------------- PLACE ORDER --------------------
@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT restaurant_id, rest_name FROM Restaurant")
    restaurants = cursor.fetchall()
    cursor.execute("SELECT item_id, item_name, price FROM MenuItem")
    items = cursor.fetchall()

    if request.method == 'POST':
        customer_id = 1
        restaurant_id = request.form['restaurant']
        item_id = request.form['item']
        quantity = int(request.form['quantity'])

        cursor.execute("SELECT price FROM MenuItem WHERE item_id = %s", (item_id,))
        price = cursor.fetchone()[0]
        subtotal = price * quantity

        cursor.execute("""
            INSERT INTO Orders (customer_id, restaurant_id, order_date, status, total_amt)
            VALUES (%s, %s, CURDATE(), 'Pending', %s)
        """, (customer_id, restaurant_id, subtotal))
        conn.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        order_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO OrderItem (order_id, item_id, quantity, subtotal)
            VALUES (%s, %s, %s, %s)
        """, (order_id, item_id, quantity, subtotal))
        conn.commit()

        cursor.close()
        conn.close()
        flash("Order placed! Proceed to payment.", "info")
        return redirect(url_for('payment', order_id=order_id))

    cursor.close()
    conn.close()
    return render_template('place_order.html', restaurants=restaurants, items=items)


# -------------------- PAYMENT --------------------
@app.route('/payment/<int:order_id>', methods=['GET', 'POST'])
def payment(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    assigned_partner = None
    paid = False

    if request.method == 'POST':
        pay_method = request.form['method']
        cursor.execute("""
            INSERT INTO Payment (order_id, pay_method, pay_status, transaction_date)
            VALUES (%s, %s, 'Paid', CURDATE())
        """, (order_id, pay_method))
        conn.commit()

        cursor.callproc('PlaceNewOrder', [order_id])
        conn.commit()

        for result in cursor.stored_results():
            data = result.fetchone()
            if data:
                assigned_partner = data[1]

        paid = True
    cursor.close()
    conn.close()
    return render_template('payment.html', order_id=order_id, paid=paid, partner_id=assigned_partner)


# -------------------- REVIEW RESTAURANT --------------------
@app.route('/review', methods=['GET', 'POST'])
def review_restaurant():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT restaurant_id, rest_name FROM Restaurant")
    restaurants = cursor.fetchall()

    if request.method == 'POST':
        restaurant_id = request.form['restaurant']
        customer_id = 1
        rating = int(request.form['rating'])
        comment = request.form['comment']

        cursor.execute("""
            INSERT INTO Review (order_id, customer_id, restaurant_id, rating, comment, review_date)
            VALUES (NULL, %s, %s, %s, %s, CURDATE())
        """, (customer_id, restaurant_id, rating, comment))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Thank you for your review!", "success")
        return redirect(url_for('dashboard'))

    cursor.close()
    conn.close()
    return render_template('review.html', restaurants=restaurants)


# -------------------- ANALYTICS --------------------
@app.route('/analytics')
def analytics():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.rest_name, 
               ROUND(AVG(rv.rating), 2) AS avg_rating,
               COUNT(rv.review_id) AS total_reviews
        FROM Restaurant r
        LEFT JOIN Review rv ON r.restaurant_id = rv.restaurant_id
        GROUP BY r.rest_name
        ORDER BY avg_rating DESC;
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('analytics.html', results=results)


# -------------------- TOP RESTAURANTS (NESTED QUERY) --------------------
@app.route('/top_restaurants')
def top_restaurants():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.rest_name, ROUND(AVG(rv.rating), 2) AS avg_rating
        FROM Review rv
        JOIN Restaurant r ON rv.restaurant_id = r.restaurant_id
        GROUP BY r.restaurant_id
        HAVING avg_rating > (
            SELECT AVG(rating) FROM Review
        )
        ORDER BY avg_rating DESC;
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('top_restaurants.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
