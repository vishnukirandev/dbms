from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

application = Flask(__name__)
application.secret_key = 'your_secret_key'

# ----------- DB SETUP ON FIRST RUN -----------
if not os.path.exists('db.sqlite3'):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    # Create 'cds' table
    c.execute('''
        CREATE TABLE cds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            is_rented INTEGER DEFAULT 0,
            rented_by TEXT
        )
    ''')

    # Create 'users' table
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Add sample data
    c.executemany('INSERT INTO cds (title, is_rented, rented_by) VALUES (?, 0, ?)', [
        ('Persona 5 - Soundtrack Collection', None),
        ('Tokyo Ghoul Season-1 Eng Sub', None),
        ('God of War - Chains of Olympus', None),
        ('Kanye West - Niggas in Paris', None)
    ])

    conn.commit()
    conn.close()


# ----------- ROUTES -----------
@application.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    with sqlite3.connect('db.sqlite3') as conn:
        cds = conn.execute('SELECT id, title, is_rented, rented_by FROM cds').fetchall()

    return render_template('home.html', cds=cds, user=session['user'])


@application.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('db.sqlite3')
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (user, pwd))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already taken!"
        session['user'] = user
        return redirect('/')
    return render_template('signup.html')


@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        conn = sqlite3.connect('db.sqlite3')
        result = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (user, pwd)).fetchone()
        if result:
            session['user'] = user
            return redirect('/')
        else:
            return "Invalid credentials!"
    return render_template('login.html')


@application.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


@application.route('/rent/<int:cd_id>')
def rent(cd_id):
    if 'user' not in session:
        return redirect('/login')

    user = session['user']

    with sqlite3.connect('db.sqlite3') as conn:
        conn.execute('UPDATE cds SET is_rented = 1, rented_by = ? WHERE id = ?', (user, cd_id))
        conn.commit()

    return redirect('/')


@application.route('/return/<int:cd_id>')
def return_cd(cd_id):
    if 'user' not in session:
        return redirect('/login')

    user = session['user']

    with sqlite3.connect('db.sqlite3') as conn:
        cd = conn.execute('SELECT rented_by FROM cds WHERE id = ?', (cd_id,)).fetchone()
        if cd and cd[0] == user:
            conn.execute('UPDATE cds SET is_rented = 0, rented_by = NULL WHERE id = ?', (cd_id,))
            conn.commit()

    return redirect('/')


# ----------- RUN -----------
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
