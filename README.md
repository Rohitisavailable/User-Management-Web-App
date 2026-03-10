# User-Management-Web-App

A secure web application for managing employees built with Flask and SQLite.

## Description

This is an Employee Management System with user authentication that allows you to register an account, log in securely, and manage employee information. The application provides a secure interface with password hashing for managing employee data including names, email addresses, and departments.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Backend programming language |
| **Flask** | Web framework for building the application |
| **Werkzeug** | Security utilities for password hashing and verification |
| **SQLite** | Lightweight database for storing user and employee data |
| **Jinja2** | Template engine for rendering HTML pages |
| **HTML5** | Frontend markup structure |
| **CSS3** | Styling and layout |

## Project Structure

```
User-Management-Web-App/
├── README.md
├── app.py                  # Main Flask application
├── database.db             # SQLite database file
├── requirements.txt        # Python dependencies
├── static/
│   └── style.css           # CSS styles
└── templates/
    ├── home.html           # Homepage
    ├── register.html       # User registration page
    ├── login.html          # User login page
    ├── employee.html       # Employee list page
    ├── add_employee.html   # Add employee form
    ├── edit_employee.html  # Edit employee form
    └── dashboard.html      # Dashboard (optional)
```

## Project Flow

1. **User Access** → User navigates to the homepage (`/`)
2. **User Registration** → New users can register an account at `/register`
3. **Password Hashing** → Passwords are securely hashed using PBKDF2:SHA256
4. **User Login** → Registered users log in at `/login` with credentials verification
5. **Session Management** → Authenticated users are granted a session
6. **Employee Management** → Users can add, view, edit, and delete employees at `/employee`
7. **Data Persistence** → All user and employee data is stored in SQLite database
8. **Logout** → Users can log out to end their session



## Features

- ✅ User Registration and Account Creation
- ✅ Secure Login with Password Hashing (PBKDF2:SHA256)
- ✅ Session Management for Authenticated Users
- ✅ Add New Employees with Name, Email, and Department
- ✅ View All Employees in a Table
- ✅ Edit Employee Information
- ✅ Delete Employees
- ✅ User Logout Functionality
- ✅ Clean and Responsive UI
- ✅ SQLite Database for Persistent Storage

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

6. **Create an Account and Login**
   - Visit http://127.0.0.1:5000/register to create a new account
   - Log in with your credentials at http://127.0.0.1:5000/login
   - Start managing employees!