from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')