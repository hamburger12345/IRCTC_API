# Railway Management System

Railway Management System is a web application built with Flask, a lightweight Python web framework. It provides functionalities similar to IRCTC, allowing users to check train availability, book seats, and manage bookings. The application also includes role-based access control, with separate privileges for administrators and regular users.

## Features

- User registration and authentication
- Role-based access control (admin and regular user roles)
- Adding new trains with source and destination
- Checking seat availability between stations
- Booking seats on trains
- Viewing booking details for users

## Tech Stack

- Python Flask: Web framework for building the application
- SQLAlchemy: Python SQL toolkit and Object-Relational Mapping (ORM) library
- Flask-JWT-Extended: JWT token-based authentication
- MySQL: Relational database management system
- HTML/CSS: Frontend for user interface
- JavaScript (optional): For dynamic frontend interactions

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/railway-management-system.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
   - Create a MySQL database and note down the connection URI.
   - Update the `SQLALCHEMY_DATABASE_URI` in `config.py` with your MySQL connection URI.

4. Run the application:

```bash
python run.py
```

5. Access the application in your web browser at http://localhost:5000.

## Configuration

- `config.py`: Contains configuration settings for the application, including database URI, secret keys, and environment-specific options.
- `app.py`: Main entry point of the application. Creates the Flask app instance and initializes database connections.
- `models.py`: Defines SQLAlchemy models for database tables.
- `routes.py`: Contains route definitions for handling HTTP requests and serving web pages.
- `auth.py`: Includes authentication-related functionality, such as user registration, login, and JWT token generation.
- `utils.py`: Utility functions used throughout the application.
- `run.py`: Script to run the Flask application.
