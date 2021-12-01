import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
import flask
from flask.wrappers import Request
from flask.sessions import NullSession
import random
import string
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

shortener_base_url = 'http://127.0.0.1:5000/'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    all_urls = conn.execute('SELECT * FROM urls').fetchall()
    conn.close()
    return render_template('index.html', existing_urls=all_urls)


@app.route('/create', methods=('GET', 'POST'))
def create():
    generated_url = generate()
    if request.method == 'POST':
        short_url = request.form['short_url']
        long_url = request.form['long_url']
        
        print(long_url)
        if not long_url:           
            flash('Check the URL!') 
        elif long_url.startswith('http://'):
            flash('Use HTTPS only!')
        elif not re.search("^https://.*\..*", long_url):
            flash('Check the URL format!')
        else:
            conn = get_db_connection()

            insert_url = conn.execute('INSERT INTO urls (short_url, long_url) VALUES (?, ?)',
                (short_url, long_url))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

        

    
    return render_template('url/create.html', generated_url=generated_url)

@app.route('/generate')
def generate(size=8, chars=string.ascii_lowercase + string.digits):
    generated_url = ""
    while not generated_url:
        short_url = shortener_base_url + ''.join(random.choice(chars) for _ in range(size))
        conn = get_db_connection()

        search_url = conn.execute('SELECT * FROM urls WHERE short_url = ?',
                        (short_url,)).fetchone()

        
        if search_url is None:
            generated_url = short_url

    conn.commit()
    conn.close()
    return generated_url

@app.route('/<path:path>')
def found(path):
    print(path)
    url = shortener_base_url + path
    print(url)
    conn = get_db_connection()
    search_url = conn.execute('SELECT long_url FROM urls WHERE short_url = ?',
                        (url,)).fetchall()

    conn.close()
    #print(search_url[0]['long_url'])
    if search_url is None:
        return redirect(url_for('index'))
    elif search_url is not None:
        return redirect(search_url[0]['long_url'])
    return path
