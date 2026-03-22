# User-Management-Web-App

A secure Flask-based employee management system with role-based access control, session authentication, and RESTful API endpoints.

## Description

This application provides a complete employee management system with two distinct user roles (admin and regular user). Users can register, authenticate, and manage employee records based on their assigned role. The system enforces role-based access at both the web UI and API levels, ensuring data security and proper authorization.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.13** | Backend programming language |
| **Flask** | Lightweight WSGI web framework |
| **Werkzeug** | Provides password hashing and verification utilities |
| **SQLite** | Lightweight relational database |
| **Jinja2** | Template engine for dynamic HTML rendering |
| **HTML5 + CSS3** | Frontend structure and styling |
| **Bootstrap 5** | Responsive UI framework |

## Role-Based Access Control (RBAC)

The application implements role-based authorization with two roles:

### Admin Role
- ✅ Full CRUD operations on employees (Create, Read, Update, Delete)
- ✅ Access to admin dashboard to view all users and statistics
- ✅ Full REST API write access (POST, PUT, DELETE)
- ✅ Seeded admin account: **username: `admin`**, **password: `admin123`**

### User Role (Default)
- ✅ View-only access to employee list
- ✅ No ability to add, edit, or delete employees
- ✅ Read-only REST API access (GET)
- ✅ Access to API documentation

### Access Control Flow
```
User Registration → Assign Role (admin/user)
                 ↓
User Login → Set Session with Role
         ↓
Route Handler → Check Role Decorator
             ↓ (admin_required / login_required)
             ↓
Access Granted / Access Denied → Redirect
```

## REST API Endpoints

All API endpoints require session authentication (login first).

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/login` | Login and create session | ❌ No |
| `POST` | `/api/logout` | Logout and clear session | ✅ Yes |

### Employee Endpoints
| Method | Endpoint | Description | Role Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/employees` | List all employees | User/Admin (read-only) |
| `POST` | `/api/employees` | Create new employee | Admin only |
| `GET` | `/api/employees/<id>` | Get single employee | User/Admin (read-only) |
| `PUT` | `/api/employees/<id>` | Update employee | Admin only |
| `DELETE` | `/api/employees/<id>` | Delete employee | Admin only |


## Security Flow

```
flowchart TD
    A[User Request] --> B{Session Token Present?}

    B -- No --> C[Redirect to /login]
    B -- Yes --> D{Session Valid?}

    D -- No --> E[Return 401 Unauthorized]
    D -- Yes --> F{Check User Role}

    F -- Admin --> G{Admin Route Required?}
    F -- User --> H{Login Required Route?}

    G -- Yes --> I[Allow Access]
    G -- No --> J[Return 403 Forbidden]

    H -- Yes --> I
    H -- No --> J

    I --> K[Process Request]
    K --> L[Return Response/Data]
```

## Project Structure

```
User-Management-Web-App/
├── README.md                   # Project documentation
├── app.py                      # Main Flask application
├── database.db                 # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
├── static/
│   └── style.css              # CSS styling
└── templates/
    ├── home.html              # Welcome page
    ├── register.html          # User registration
    ├── login.html             # User login
    ├── employee.html          # Employee list (with role checks)
    ├── add_employee.html      # Add employee form (admin only)
    ├── edit_employee.html     # Edit employee form (admin only)
    ├── admin_dashboard.html   # Admin statistics and user list
    └── api_docs.html          # API documentation
```

## Features

- ✅ User registration with role assignment
- ✅ Secure login with PBKDF2:SHA256 password hashing
- ✅ Session-based authentication and authorization
- ✅ Role-based access control (admin/user)
- ✅ Employee CRUD operations (restricted by role)
- ✅ Admin dashboard with statistics
- ✅ RESTful API with JSON responses
- ✅ Input validation and error handling
- ✅ Responsive Bootstrap UI
- ✅ SQLite persistent storage

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rohitisavailable/User-Management-Web-App.git
   cd User-Management-Web-App
   ```

2. **Create and activate a virtual environment (optional but recommended)**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://127.0.0.1:5000/
   ```

## Default Admin Account

The application comes pre-seeded with an admin account:
- **Username:** `admin`
- **Password:** `admin123`

Use this to log in and explore admin features like the admin dashboard and employee management.

## API Testing

Access API documentation at:
```
http://127.0.0.1:5000/api/docs
```

Example workflow:
1. Register a new user at `/register`
2. Login at `/api/login` with JSON credentials
3. Make API requests to `/api/employees`
