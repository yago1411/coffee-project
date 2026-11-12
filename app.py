import os
import time
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'coffee_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres')
    )


def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS brews (
                    id SERIAL PRIMARY KEY,
                    bean_name VARCHAR(100) NOT NULL,
                    method VARCHAR(50) NOT NULL,
                    grind_size VARCHAR(50),
                    rating INT,
                    notes TEXT
                );
            ''')
            conn.commit()
            cur.close()
            conn.close()
            print("Database table created successfully.")
            break
        except Exception as e:
            print(f"Waiting for database... Remaining retries: {retries}")
            time.sleep(2)
            retries -= 1

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM brews ORDER BY id DESC;')
    brews = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', brews=brews)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        bean_name = request.form['bean_name']
        method = request.form['method']
        grind_size = request.form['grind_size']
        rating = request.form['rating']
        notes = request.form['notes']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO brews (bean_name, method, grind_size, rating, notes) VALUES (%s, %s, %s, %s, %s)',
                    (bean_name, method, grind_size, rating, notes))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
