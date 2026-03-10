# User-Management-Web-App

A simple web application for managing users built with Flask and SQLite.

## Description

This is an Employee Management System built with Flask and SQLite. It features user authentication (login/register), session-based access control, and full CRUD operations for managing employee records. Users must register an account and log in to access the employee management dashboard.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Backend programming language |
| **Flask** | Web framework for building the application |
| **SQLite** | Lightweight database for storing user and employee data |
| **Jinja2** | Template engine for rendering HTML pages |
| **Werkzeug** | Security utilities for password hashing and verification |
| **HTML5** | Frontend markup structure |
| **CSS3** | Styling and layout |

## Project Structure

```
User-Management-Web-App/
├── README.md
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── database.db            # SQLite database file
├── static/
│   └── style.css          # CSS styles
└── templates/
    ├── home.html          # Home page
    ├── register.html      # User registration page
    ├── login.html         # User login page
    ├── employee.html      # Employee list display
    ├── add_employee.html  # Add new employee form
    ├── edit_employee.html # Edit employee form
    └── dashboard.html     # Dashboard (currently unused)
```

## Project Flow

1. **User Access** → User navigates to the homepage (`/`)
2. **Authentication** → User registers (`/register`) or logs in (`/login`) with secure password hashing
3. **Session Creation** → Upon successful login, user session is created
4. **Dashboard Access** → Authenticated user accesses employee dashboard (`/employee`)
5. **View Employees** → Application fetches all employees from SQLite database and displays them in a table
6. **Manage Employees** → User can:
   - Add new employee (`/add-employee`)
   - Edit employee details (`/edit/<id>`)
   - Delete employee (`/delete/<id>`)
7. **Data Persistence** → All changes are saved to SQLite database
8. **Logout** → User can logout to end session and return to homepage
## Flowchart



## Features

- ✅ User registration with secure password hashing (PBKDF2)
- ✅ User login with session management
- ✅ Add new employees with name, email, and department
- ✅ View all employees in a table format
- ✅ Edit employee information
- ✅ Delete employees from the system
- ✅ Session-based access control (protected routes)
- ✅ Clean and responsive UI
- ✅ SQLite database for persistent storage
- ✅ Logout functionality

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rohitisavailable/User-Management-Web-App.git
   cd User-Management-Web-App
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or manually install:
   ```bash
   pip install flask werkzeug
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://127.0.0.1:5000/
   ```

5. **Create an account and start managing employees**
   - Click on "Register" to create a new account
   - Log in with your credentials
   - Begin adding and managing employee records