# FastAPI Appointment Booking System

A robust, REST API appointment booking system built with FastAPI. This application allows doctors to register, manage their availability, and handle appointments scheduled by patients.

## Features

- Doctor registration with work experience and academic history
- Patient registration and profile management
- Doctor availability management
- Appointment booking, cancellation, and rescheduling
- JWT authentication and authorization
- API documentation with Swagger UI
- Database migrations with Alembic

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- SQLite (default) or PostgreSQL (optional)

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Moshood-Wale/booking-system.git
cd booking-system
```

### 2. Create and activate a virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
DATABASE_URL=sqlite:///./app.db
# For PostgreSQL use: postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
```

### 5. Run migrations

```bash
alembic upgrade head
```

### 6. Start the application

```bash
uvicorn app.main:app --reload
```

The application will be available at http://localhost:8000

## API Documentation

Interactive API documentation is available at:
- Swagger UI: http://localhost:8000/api/docs/
- OpenAPI Schema: http://localhost:8000/api/schema/

## Database Options

### SQLite (Default)

The project is configured to use SQLite by default, which stores data in a file named `app.db`. No additional setup is required.

### PostgreSQL (Recommended for Production)

For production environments, PostgreSQL is recommended:

1. Install PostgreSQL and create a database
2. Install the additional dependency:
   ```bash
   pip install psycopg2-binary
   ```
3. Update your `.env` file with the PostgreSQL connection string:
   ```
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```
4. Run migrations:
   ```bash
   alembic upgrade head
   ```

## Docker Setup

The project includes Docker configuration for easy deployment:

```bash
# Build and start the services
docker-compose up --build

# To run in detached mode
docker-compose up -d
```

## API Testing Guide

### Authentication

To access protected endpoints, you'll need to:

1. Register as a doctor or patient
2. Obtain a JWT token via the login endpoint
3. Include the token in the Authorization header:
   ```
   Authorization: Bearer your_token_here
   ```

### Example API Flows

#### Doctor Registration Flow:

1. Register a doctor:
   ```
   POST /api/v1/doctors/
   ```
2. Login as doctor:
   ```
   POST /api/v1/auth/login
   ```
3. Set up availability:
   ```
   POST /api/v1/availabilities/
   ```

#### Patient Booking Flow:

1. Register a patient:
   ```
   POST /api/v1/patients/
   ```
2. Login as patient:
   ```
   POST /api/v1/auth/login
   ```
3. View doctor availabilities:
   ```
   GET /api/v1/availabilities/doctor/{doctor_id}
   ```
4. Book an appointment:
   ```
   POST /api/v1/appointments/
   ```

## Project Structure

```
fastapi_appointment_system/
│
├── app/
│   ├── __init__.py
│   ├── main.py             # Application entry point
│   ├── database.py         # Database configuration
│   ├── config.py           # Application settings
│   ├── api/                # API endpoints
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   └── core/               # Core functionality
│
├── alembic/                # Database migrations
├── tests/                  # Unit and integration tests
├── .env                    # Environment variables
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
└── requirements.txt        # Python dependencies
```

## Development Notes

- **Database Access**: The application uses SQLAlchemy as an ORM with a dependency injection pattern
- **Authentication**: JWT tokens are used for authentication with role-based access control
- **Data Validation**: Pydantic models provide validation and serialization
- **API Design**: The API follows RESTful principles with proper status codes and response models

## License

This project is licensed under the MIT License 
