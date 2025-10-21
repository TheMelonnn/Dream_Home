from flask import Flask, redirect, request, url_for
from flask import render_template
import sqlite3

app = Flask(__name__)
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

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
    conn.close()

    if room is None:
        return "Room not found", 404  # atau bisa juga redirect(url_for('dashboard'))

    return render_template('room.html', room_name=room['name'])


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
