from flask import Flask, redirect, request, url_for, render_template
from webcrawling import crawl_web_ikea, crawl_web_ruparupa, crawl_web_ufoelektronika
import sqlite3
import validators
from datetime import datetime, timedelta
import time
import sys
from portofoliocrawling import run_crawl

app = Flask(__name__)
# app.debug = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True

DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE, check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA BUSY_TIMEOUT=10000;")
    return conn

def safe_execute(conn, query, params=(), retries=3):
    for i in range(retries):
        try:
            conn.execute(query, params)
            conn.commit()
            return
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print(f"[WARN] Database locked, retrying ({i+1}/{retries})...")
                time.sleep(1)
            else:
                raise

def update_products(room_id):
    # Jika tidak ada koneksi dikirim, buat baru dan tandai untuk ditutup
    conn = None

    try:
        conn = get_db_connection()
        # Gunakan cursor lokal
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE room_id = ?", (room_id,))
        products = cur.fetchall()

        for p in products:
            url = p['product_url']
            product_id = p['id']
            updated_data = None

            if 'ruparupa' in url:
                updated_data = crawl_web_ruparupa(url)
            elif 'ikea' in url:
                updated_data = crawl_web_ikea(url)
            elif 'ufoelektronika' in url:
                updated_data = crawl_web_ufoelektronika(url)

            if not updated_data:
                continue

            if isinstance(updated_data, tuple):
                name, price, image = updated_data
            else:
                name, price, image = (
                    updated_data.get('name'),
                    updated_data.get('price'),
                    updated_data.get('image')
                )

            cur.execute("""
                UPDATE products 
                SET name = ?, price = ?, image_url = ?
                WHERE id = ?
            """, (name, price, image, product_id))

            print(f"UPDATED")

        # Update last_updated di tabel rooms
        now = datetime.now().isoformat()
        cur.execute("""
            UPDATE rooms SET last_updated = ?
            WHERE id = ?
        """, (now, room_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"[ERROR] update_products failed: {e}")
    finally:
        if conn:
            conn.close()



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
    room = conn.execute(
        'SELECT * FROM rooms WHERE name = ?', 
        (room_name.replace('-', ' '),)
    ).fetchone()

    if room is None:
        conn.close()
        return "Room not found", 404

    last_updated = room['last_updated']
    now = datetime.now()

    should_update = False
    if not last_updated:
        should_update = True
    else:
        try:
            last_updated_dt = datetime.fromisoformat(last_updated)
            if now - last_updated_dt > timedelta(minutes=30):
                should_update = True
        except:
            should_update = True

    if should_update:
        print(f"[UPDATE TRIGGERED] Updating products for room: {room_name}")
        update_products(room['id'])
    else:
        print(f"[SKIPPED] No update needed for room: {room_name}")

    products = conn.execute(
        'SELECT * FROM products WHERE room_id = ?', 
        (room['id'],)
    ).fetchall()

    grand_total = sum(product['price'] * product['quantity'] for product in products)
    conn.close()

    return render_template('room.html', room_name=room['name'], products=products, grand_total=grand_total)


@app.route('/add_room', methods=['POST'])
def add_room():
    room_name = request.form['room_name']
    conn = get_db_connection()
    safe_execute(conn, 'INSERT INTO rooms (name) VALUES (?)', (room_name,))
    # conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    conn = get_db_connection()
    safe_execute(conn, 'DELETE FROM rooms WHERE id = ?', (room_id,))
    # conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/<room_name>/add-product', methods=['GET', 'POST'])
def add_product(room_name):
    product = None
    error = None

    if request.method == 'POST':
        link = request.form['product_url']
        source = request.form['source']

        if not validators.url(link):
            error = "URL tidak valid!"
            return render_template("add-product.html", room_name=room_name, error=error)

        try:
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
            else:
                error = f"Gagal mengambil data dari {source}. Silakan periksa URL atau coba lagi."

        except Exception:
            error = "Terjadi kesalahan saat mengambil data produk."
            return render_template("add-product.html", room_name=room_name, error=error)

    return render_template('add-product.html', room_name=room_name, product=product, error=error)


@app.route('/<room_name>/save-product', methods=['POST'])
def save_product(room_name):
    conn = get_db_connection()
    room = conn.execute('SELECT id FROM rooms WHERE name = ?', (room_name,)).fetchone()

    if room:
        type_value = request.form['type'] or 'lainnya'
        safe_execute(conn, '''
            INSERT INTO products (room_id, name, price, product_url, image_url, quantity, type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            room['id'],
            request.form['name'],
            request.form['price'],
            request.form['product_url'],
            request.form['image'],
            request.form.get('quantity', 1),
            type_value
        ))
        # conn.commit()

    conn.close()
    return redirect(url_for('room_page', room_name=room_name))


@app.route('/delete-product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()
    safe_execute(conn, 'DELETE FROM products WHERE id = ?', (product_id,))
    # conn.commit()
    conn.close()
    return '', 204

@app.route('/update-portfolio')
def run():
    try:
        run_crawl()
        return render_template("updateportofolio.html", status="update success")
    except Exception as e:
        return f"<p>Update failed: {e}</p>", 500


if __name__ == '__main__':
    init_db()
    app.run()
