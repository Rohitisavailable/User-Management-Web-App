# User-Management-Web-App

A web application for user authentication and management built with Flask, SQLite, and Bootstrap 5.

## Description

This is a User Management System that provides user registration, login, and a protected dashboard. The application uses session-based authentication with secure password hashing to manage user access.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Backend programming language |
| **Flask** | Web framework for building the application |
| **SQLite** | Lightweight database for storing user data |
| **Werkzeug** | Password hashing and security utilities |
| **Jinja2** | Template engine for rendering HTML pages |
| **Bootstrap 5** | Frontend UI framework for responsive design |
| **HTML5** | Frontend markup structure |
| **CSS3** | Custom styling and layout |

## Project Structure

```
User-Management-Web-App/
├── README.md
├── app.py                  # Main Flask application
├── database.db             # SQLite database file
├── requirements.txt        # Python dependencies
├── static/
│   └── style.css           # Custom CSS styles
└── templates/
    ├── home.html           # Landing page with login/register links
    ├── register.html       # User registration form
    ├── login.html          # User login form
    └── dashboard.html      # Protected dashboard page
```

## Project Flow

1. **Home Page** → User navigates to the homepage (`/`) and sees options to Login or Register
2. **Register** → New user fills in username and password at `/register`
3. **Account Creation** → Password is securely hashed and stored in the SQLite database
4. **Login** → User logs in at `/login` with their credentials
5. **Authentication** → Flask backend verifies credentials against the hashed password
6. **Dashboard** → Authenticated user is redirected to the protected dashboard (`/dashboard`)
7. **Logout** → User can log out (`/logout`), which clears the session and redirects to home

## User Authentication Flow

flowchart TD

A[Start Application] --> B{User Action}

B -->|Register| C[Open Register Page]
C --> D[Enter Username & Password]
D --> E[Hash Password]
E --> F[Save User in SQLite Database]
F --> G[Redirect to Login]

B -->|Login| H[Open Login Page]
H --> I[Enter Credentials]
I --> J[Fetch User From Database]

J --> K{Password Match?}

K -->|No| H

K -->|Yes| L[Create Session]
L --> M[Redirect Dashboard]

M --> N{User Click Logout?}

N -->|Yes| O[Destroy Session]
O --> H

N -->|No| M

## Features

- ✅ User registration with username and password
- ✅ Secure password hashing using Werkzeug
- ✅ Session-based user authentication
- ✅ Protected dashboard accessible only to logged-in users
- ✅ Logout functionality with session clearing
- ✅ Responsive UI with Bootstrap 5
- ✅ SQLite database for persistent storage

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

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://127.0.0.1:5000/
   ```
