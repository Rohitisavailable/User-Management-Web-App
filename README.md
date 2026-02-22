# User-Management-Web-App

A simple web application for managing users built with Flask and SQLite.

## Description

This is a User Management System that allows you to add and view users. The application provides a clean, simple interface for managing user information including names and email addresses.

## Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Backend programming language |
| **Flask** | Web framework for building the application |
| **SQLite** | Lightweight database for storing user data |
| **Jinja2** | Template engine for rendering HTML pages |
| **HTML5** | Frontend markup structure |
| **CSS3** | Styling and layout |

## Project Structure

```
User-Management-Web-App/
├── README.md
└── User-Manage/
    ├── app.py              # Main Flask application
    ├── database.db         # SQLite database file
    ├── static/
    │   └── style.css       # CSS styles
    └── templates/
        └── index.html      # HTML template
```

## Project Flow

1. **User Access** → User navigates to the homepage (`/`)
2. **View Users** → Application fetches all users from SQLite database and displays them in a table
3. **Add User** → User fills in the form with name and email
4. **Form Submission** → Data is sent via POST request to the server
5. **Database Insert** → Flask backend inserts the new user into the SQLite database
6. **Redirect** → User is redirected back to the homepage to see the updated user list

## Features

- ✅ Add new users with name and email
- ✅ View all registered users in a table
- ✅ Clean and responsive UI
- ✅ SQLite database for persistent storage

## How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rohitisavailable/User-Management-Web-App.git
   cd User-Management-Web-App/User-Manage
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://127.0.0.1:5000/
   ```