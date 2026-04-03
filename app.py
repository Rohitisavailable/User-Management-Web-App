import os
import re
import secrets
import sqlite3
from datetime import timedelta
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config.update(
    SECRET_KEY=(
        os.environ.get("FLASK_SECRET_KEY")
        or os.environ.get("SECRET_KEY")
        or secrets.token_hex(32)
    ),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=(
        os.environ.get("SESSION_COOKIE_SECURE", "0") == "1"
        or os.environ.get("FLASK_ENV") == "production"
    ),
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
)

CSRF_SESSION_KEY = "_csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    try:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            )
            """
        )
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS employee (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                dept TEXT NOT NULL
            )
            """
        )
        db.commit()

        user_columns = [
            column["name"]
            for column in db.execute("PRAGMA table_info(users)").fetchall()
        ]
        if "role" not in user_columns:
            db.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'user'")
            db.commit()

        db.execute(
            "UPDATE users SET role = 'user' WHERE role IS NULL OR TRIM(role) = ''"
        )
        db.commit()

        admin_exists = db.execute(
            "SELECT id FROM users WHERE username = ?",
            ("admin",)
        ).fetchone()
        if not admin_exists:
            default_admin_password = os.environ.get("DEFAULT_ADMIN_PASSWORD", "").strip()
            if not default_admin_password:
                app.logger.warning(
                    "DEFAULT_ADMIN_PASSWORD is not set; skipping automatic admin user creation."
                )
                return

            admin_password_hash = generate_password_hash(
                default_admin_password,
                method="pbkdf2:sha256",
                salt_length=16
            )
            db.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("admin", admin_password_hash, "admin")
            )
            db.commit()
    finally:
        db.close()

def is_password_hash(password_value):
    return isinstance(password_value, str) and (
        password_value.startswith("pbkdf2:")
        or password_value.startswith("scrypt:")
        or password_value.startswith("argon2:")
    )

def normalize_role(role_value):
    return "admin" if role_value == "admin" else "user"


def get_or_create_csrf_token():
    csrf_token = session.get(CSRF_SESSION_KEY)
    if not csrf_token:
        csrf_token = secrets.token_urlsafe(32)
        session[CSRF_SESSION_KEY] = csrf_token
    return csrf_token


@app.context_processor
def inject_csrf_token():
    return {"csrf_token": get_or_create_csrf_token()}


@app.before_request
def verify_csrf_token_for_unsafe_methods():
    if request.method in {"GET", "HEAD", "OPTIONS", "TRACE"}:
        return None

    if request.endpoint == "static":
        return None

    if request.endpoint in {"api_login"}:
        return None

    expected_token = session.get(CSRF_SESSION_KEY)
    if request.path.startswith("/api/"):
        provided_token = request.headers.get(CSRF_HEADER_NAME, "")
    else:
        provided_token = request.form.get("csrf_token", "")

    if (
        not expected_token
        or not provided_token
        or not secrets.compare_digest(str(provided_token), str(expected_token))
    ):
        if request.path.startswith("/api/"):
            return jsonify({"error": "CSRF validation failed."}), 400
        return "CSRF validation failed.", 400

    return None


@app.after_request
def apply_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

def employee_row_to_dict(employee_row):
    return {
        "id": employee_row["id"],
        "name": employee_row["name"],
        "email": employee_row["email"],
        "dept": employee_row["dept"],
    }

def validate_employee_payload(payload):
    required_fields = ("name", "email", "dept")
    missing_fields = [
        field for field in required_fields
        if not str(payload.get(field, "")).strip()
    ]
    if missing_fields:
        return None, f"Missing required fields: {', '.join(missing_fields)}"

    clean_payload = {
        "name": str(payload.get("name", "")).strip(),
        "email": str(payload.get("email", "")).strip().lower(),
        "dept": str(payload.get("dept", "")).strip(),
    }
    if not EMAIL_REGEX.match(clean_payload["email"]):
        return None, "Email format is invalid."

    return clean_payload, None

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)

    return wrapped_view

def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            return redirect(url_for("employee"))
        return view_func(*args, **kwargs)

    return wrapped_view

def api_login_required():
    if "user" not in session:
        return jsonify({"error": "Authentication required."}), 401
    return None

def api_admin_required():
    auth_error = api_login_required()
    if auth_error:
        return auth_error
    if session.get("role") != "admin":
        return jsonify({"error": "Admin role required."}), 403
    return None

@app.route('/')
def home():
    return render_template(
        'home.html',
        session_user=session.get("user"),
        session_role=session.get("role", "user")
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        raw_password = request.form.get('password', '').strip()
        role = 'user'

        if not username or not raw_password:
            return render_template('register.html', error='Username and password are required.')

        password_hash = generate_password_hash(
            raw_password,
            method='pbkdf2:sha256',
            salt_length=16
        )

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password_hash, role)
            )
            db.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            error = 'Username already exists. Choose a different username.'
        finally:
            db.close()

    return render_template('register.html', error=error)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_employee(id):
    db = get_db()
    employee = db.execute(
        "SELECT * FROM employee WHERE id = ?", (id,)
    ).fetchone()

    if not employee:
        db.close()
        return redirect('/employee')

    error = None
    if request.method == 'POST':
        clean_payload, error = validate_employee_payload(
            {
                'name': request.form.get('name', ''),
                'email': request.form.get('email', ''),
                'dept': request.form.get('dept', ''),
            }
        )

        if not error:
            try:
                db.execute(
                    "UPDATE employee SET name=?, email=?, dept=? WHERE id=?",
                    (
                        clean_payload['name'],
                        clean_payload['email'],
                        clean_payload['dept'],
                        id
                    )
                )
                db.commit()
                db.close()
                return redirect('/employee')
            except sqlite3.IntegrityError:
                error = 'Employee email already exists.'

    db.close()
    return render_template('edit_employee.html', employee=employee, error=error)

@app.route('/delete/<int:id>', methods=['POST'])
@admin_required
def delete_employee(id):
    db = get_db()
    db.execute("DELETE FROM employee WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect('/employee')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        submitted_password = request.form.get('password', '').strip()

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        db.close()

        if (
            user
            and is_password_hash(user['password'])
            and check_password_hash(user['password'], submitted_password)
        ):
            # Prevent session fixation by regenerating session state on login.
            session.clear()
            session.permanent = True
            session['user_id'] = user['id']
            session['user'] = user['username']
            session['role'] = normalize_role(user['role'])
            get_or_create_csrf_token()

            if session['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('employee'))

        error = 'Invalid username or password.'

    return render_template('login.html', error=error)


@app.route('/add-employee', methods=['GET', 'POST'])
@admin_required
def add_employee():
    error = None
    if request.method == 'POST':
        clean_payload, error = validate_employee_payload(
            {
                'name': request.form.get('name', ''),
                'email': request.form.get('email', ''),
                'dept': request.form.get('dept', ''),
            }
        )

        if not error:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO employee (name, email, dept) VALUES (?, ?, ?)",
                    (
                        clean_payload['name'],
                        clean_payload['email'],
                        clean_payload['dept'],
                    )
                )
                db.commit()
                return redirect('/employee')
            except sqlite3.IntegrityError:
                error = 'Employee email already exists.'
            finally:
                db.close()

    return render_template('add_employee.html', error=error)


@app.route('/employee')
@login_required
def employee():
    db = get_db()
    data = db.execute("SELECT * FROM employee ORDER BY id DESC").fetchall()
    db.close()
    return render_template(
        'employee.html',
        employee=data,
        session_user=session.get('user'),
        session_role=session.get('role', 'user')
    )


@app.route('/admin')
@admin_required
def admin_dashboard():
    db = get_db()
    users = db.execute(
        "SELECT id, username, role FROM users ORDER BY id DESC"
    ).fetchall()
    employee_count = db.execute("SELECT COUNT(*) AS total FROM employee").fetchone()["total"]
    user_count = db.execute("SELECT COUNT(*) AS total FROM users").fetchone()["total"]
    db.close()

    return render_template(
        'admin_dashboard.html',
        users=users,
        user_count=user_count,
        employee_count=employee_count,
        session_user=session.get('user')
    )


@app.route('/api/docs')
@login_required
def api_docs():
    return render_template('api_docs.html', session_role=session.get('role', 'user'))


@app.route('/api/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    payload = request.get_json(silent=True) or {}
    username = str(payload.get('username', '')).strip()
    submitted_password = str(payload.get('password', '')).strip()

    if not username or not submitted_password:
        return jsonify({"error": "Username and password are required."}), 400

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    db.close()

    if (
        not user
        or not is_password_hash(user['password'])
        or not check_password_hash(user['password'], submitted_password)
    ):
        return jsonify({"error": "Invalid credentials."}), 401

    session.clear()
    session.permanent = True
    session['user_id'] = user['id']
    session['user'] = user['username']
    session['role'] = normalize_role(user['role'])
    csrf_token = get_or_create_csrf_token()

    return jsonify(
        {
            "message": "Login successful.",
            "user": {
                "id": user['id'],
                "username": user['username'],
                "role": normalize_role(user['role'])
            },
            "csrf_token": csrf_token
        }
    ), 200


@app.route('/api/logout', methods=['POST'])
def api_logout():
    auth_error = api_login_required()
    if auth_error:
        return auth_error

    session.clear()
    return jsonify({"message": "Logout successful."}), 200


@app.route('/api/employees', methods=['GET', 'POST'])
def api_employees():
    if request.method == 'GET':
        auth_error = api_login_required()
        if auth_error:
            return auth_error

        db = get_db()
        employees = db.execute("SELECT * FROM employee ORDER BY id DESC").fetchall()
        db.close()
        return jsonify([employee_row_to_dict(row) for row in employees]), 200

    auth_error = api_admin_required()
    if auth_error:
        return auth_error

    if not request.is_json:
        return jsonify({"error": "Request body must be JSON."}), 400

    payload = request.get_json(silent=True) or {}
    clean_payload, error = validate_employee_payload(payload)
    if error:
        return jsonify({"error": error}), 400

    db = get_db()
    try:
        cursor = db.execute(
            "INSERT INTO employee (name, email, dept) VALUES (?, ?, ?)",
            (
                clean_payload['name'],
                clean_payload['email'],
                clean_payload['dept'],
            )
        )
        db.commit()
        created_employee = db.execute(
            "SELECT * FROM employee WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()
    except sqlite3.IntegrityError:
        db.close()
        return jsonify({"error": "Employee email already exists."}), 409

    db.close()
    return jsonify(
        {
            "message": "Employee created.",
            "employee": employee_row_to_dict(created_employee)
        }
    ), 201


@app.route('/api/employees/<int:employee_id>', methods=['GET', 'PUT', 'DELETE'])
def api_employee_detail(employee_id):
    if request.method == 'GET':
        auth_error = api_login_required()
        if auth_error:
            return auth_error

        db = get_db()
        employee = db.execute(
            "SELECT * FROM employee WHERE id = ?",
            (employee_id,)
        ).fetchone()
        db.close()
        if not employee:
            return jsonify({"error": "Employee not found."}), 404
        return jsonify(employee_row_to_dict(employee)), 200

    auth_error = api_admin_required()
    if auth_error:
        return auth_error

    db = get_db()
    existing_employee = db.execute(
        "SELECT * FROM employee WHERE id = ?",
        (employee_id,)
    ).fetchone()

    if not existing_employee:
        db.close()
        return jsonify({"error": "Employee not found."}), 404

    if request.method == 'PUT':
        if not request.is_json:
            db.close()
            return jsonify({"error": "Request body must be JSON."}), 400

        payload = request.get_json(silent=True) or {}
        clean_payload, error = validate_employee_payload(payload)
        if error:
            db.close()
            return jsonify({"error": error}), 400

        try:
            db.execute(
                "UPDATE employee SET name = ?, email = ?, dept = ? WHERE id = ?",
                (
                    clean_payload['name'],
                    clean_payload['email'],
                    clean_payload['dept'],
                    employee_id,
                )
            )
            db.commit()
        except sqlite3.IntegrityError:
            db.close()
            return jsonify({"error": "Employee email already exists."}), 409

        updated_employee = db.execute(
            "SELECT * FROM employee WHERE id = ?",
            (employee_id,)
        ).fetchone()
        db.close()
        return jsonify(
            {
                "message": "Employee updated.",
                "employee": employee_row_to_dict(updated_employee)
            }
        ), 200

    db.execute("DELETE FROM employee WHERE id = ?", (employee_id,))
    db.commit()
    db.close()
    return jsonify({"message": "Employee deleted."}), 200


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return redirect('/')


init_db()


if __name__ == '__main__':
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1")
