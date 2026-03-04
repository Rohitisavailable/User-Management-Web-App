from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "secure-secret-key"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def is_password_hash(password_value):
    return isinstance(password_value, str) and (
        password_value.startswith("pbkdf2:")
        or password_value.startswith("scrypt:")
        or password_value.startswith("argon2:")
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        raw_password = request.form['password']
        password_hash = generate_password_hash(
            raw_password,
            method='pbkdf2:sha256',
            salt_length=16
        )

        db = get_db()
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password_hash)
        )
        db.commit()
        return redirect('/login')

    return render_template('register.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if 'user' not in session:
        return redirect('/login')
    
    db = get_db()
    employee = db.execute(
        "SELECT * FROM employee WHERE id = ?", (id,)
    ).fetchone()

    if request.method == 'POST':
        db.execute(
            "UPDATE employee SET name=?, email=?, dept=? WHERE id=?",
            (
                request.form['name'],
                request.form['email'],
                request.form['dept'],
                id
            )
        )
        db.commit()
        return redirect('/employee')
    return render_template('edit_employee.html', employee=employee)

@app.route('/delete/<int:id>')
def delete_employee(id):
    if 'user' not in session:
        return redirect('/login')
    
    db = get_db()
    db.execute("DELETE FROM employee WHERE id=?", (id,))
    db.commit()
    return redirect('/employee')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        submitted_password = request.form['password']

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if (
            user
            and is_password_hash(user['password'])
            and check_password_hash(user['password'], submitted_password)
        ):
            session['user'] = user['username']
            return redirect(url_for('employee'))

    return render_template('login.html')


@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    if 'user' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dept = request.form['dept']

        db = get_db()
        db.execute(
            "INSERT INTO employee (name, email, dept) VALUES (?, ?, ?)",
            (name, email, dept)
        )
        db.commit()
        return redirect('/employee')
    return render_template('add_employee.html')


@app.route('/employee')
def employee():
    if 'user' not in session:
        return redirect('/login')
    
    db = get_db()
    data = db.execute("SELECT * FROM employee").fetchall()
    return render_template('employee.html', employee=data)


"""@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    return render_template('dashboard.html', user=session['user'])"""


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
