from flask import Flask, redirect, request, url_for
from flask import render_template
from webcrawling import crawl_web_ikea, crawl_web_ruparupa, crawl_web_ufoelektronika
import sqlite3

app = Flask(__name__)
# app.debug = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    rooms = conn.execute('SELECT id, name FROM rooms').fetchall()
    conn.close()
    return render_template('dashboard.html', rooms=rooms)

@app.route('/dashboard/<room_name>')
def room_page(room_name):
    conn = get_db_connection()
    room = conn.execute('SELECT * FROM rooms WHERE name = ?', (room_name.replace('-', ' '),)).fetchone()
    # conn.close()

    if room is None:
        return "Room not found", 404  # atau bisa juga redirect(url_for('dashboard'))

    products = conn.execute('SELECT * FROM products WHERE room_id = ?', (room['id'],)).fetchall()
    grand_total = sum(product['price'] * product['quantity'] for product in products)
    conn.close()

    return render_template('room.html', room_name=room['name'], products=products, grand_total=grand_total)

@app.route('/add_room', methods=['POST'])
def add_room():
    room_name = request.form['room_name']
    conn = get_db_connection()
    conn.execute('INSERT INTO rooms (name) VALUES (?)', (room_name,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM rooms WHERE id = ?', (room_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/<room_name>/add-product', methods=['GET', 'POST'])
def add_product(room_name):
    product = None
    if request.method == 'POST':
        link = request.form['product_url']
        source = request.form['source']

        if source == 'ikea':
            name, price, image = crawl_web_ikea(link)
        elif source == 'ruparupa':
            name, price, image = crawl_web_ruparupa(link)
        elif source == 'ufoelektronika':
            name, price, image = crawl_web_ufoelektronika(link)
        else:
            name = price = image = None

        if name and price and image:
            product = {
                'name': name,
                'price': price,
                'image': image,
                'product_url': link
            }

    return render_template('add-product.html', room_name=room_name, product=product)

@app.route('/<room_name>/save-product', methods=['POST'])
def save_product(room_name):
    conn = get_db_connection()
    room = conn.execute('SELECT id FROM rooms WHERE name = ?', (room_name,)).fetchone()

    if room:
        conn.execute('''
            INSERT INTO products (room_id, name, price, product_url, image_url, quantity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            room['id'],
            request.form['name'],
            request.form['price'],
            request.form['product_url'],   # disesuaikan dari form input
            request.form['image'],   # disesuaikan dari form input
            request.form.get('quantity', 1)   # disesuaikan dari form input
        ))
        conn.commit()

    conn.close()
    return redirect(url_for('room_page', room_name=room_name))

@app.route('/delete-product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    return '', 204

