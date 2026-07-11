# Trekking Management System

# BootcampHub - Management Application

BootcampHub is a comprehensive web application designed to streamline the management of technical bootcamps. 

## Features
* **Role-Based Access Control (RBAC):** Distinct dashboards for Admins, Mentors, and Students.
* **Analytics Dashboard:** Visual bootcamp enrollment data using Chart.js.
* **RESTful APIs:** JSON endpoints for managing bootcamps.
* **Security:** Password hashing using werkzeug.

## Setup Instructions
1. Clone repo: `git clone https://github.com/24fnaz-cyber/Trekking-Management-app`
2. Create virtual environment and activate it.
3. Install dependencies: `pip install Flask Flask-SQLAlchemy Flask-Login`
4. Run application: `python app.py`

## Default Credentials
The database seeds a default admin on the first run:
* **Username:** `admin`
* **Password:** `adminpassword`