# 3D Asset Library API

A RESTful Flask API for managing personal 3D assets. Users can register, authenticate using JSON Web Tokens (JWT), and manage their own asset collections through protected CRUD endpoints.

## Features

- User registration and login
- Secure password hashing with Flask-Bcrypt
- JWT-based authentication
- Protected API endpoints
- Create, retrieve, update, and delete 3D assets
- User-specific asset ownership and access control
- Paginated asset retrieval
- Database migrations with Flask-Migrate
- Database seeding with sample users and assets
- Automated API tests using Pytest

## Technology Stack

- Python 3.13
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-JWT-Extended
- SQLite
- Pytest

## Project Structure

```text
backend/
├── app.py
├── auth.py
├── assets.py
├── extensions.py
├── models.py
├── seed.py
├── migrations/
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── Pipfile
├── Pipfile.lock
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd flask-c10-summative-lab-sessions-and-jwt-clients/backend
```

### 2. Install Pipenv

```bash
python -m pip install pipenv
```

### 3. Install project dependencies

```bash
pipenv install
```

### 4. Set up the database

Apply the existing database migrations:

```bash
pipenv run flask --app app db upgrade
```

If setting up the database for the first time and no migration revision exists, generate one before upgrading:

```bash
pipenv run flask --app app db migrate -m "create users and assets tables"
pipenv run flask --app app db upgrade
```

### 5. Seed the database

```bash
pipenv run python seed.py
```

This creates sample users and 3D assets.

### 6. Run the application

```bash
pipenv run python app.py
```

The API will run at:

`http://localhost:5555`

## Database Models

### User

| Field | Description |
|---|---|
| id | Primary key |
| username | Unique username |
| password_hash | Securely hashed password |

### Asset

| Field | Description |
|---|---|
| id | Primary key |
| name | Asset name |
| description | Asset description |
| category | Asset category |
| format | Asset file format |
| user_id | Foreign key referencing the owner |

Supported example categories include `character`, `environment`, `material`, and `simulation`.

Example formats include `BLEND`, `FBX`, `OBJ`, and `EXR`.

## API Endpoints

All asset endpoints require a valid JWT access token.

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup` | Register a new user |
| POST | `/login` | Authenticate an existing user |
| GET | `/me` | Retrieve the authenticated user's information |

### Asset Management

| Method | Endpoint | Description |
|---|---|---|
| GET | `/assets` | Retrieve the authenticated user's assets |
| POST | `/assets` | Create a new asset |
| PATCH | `/assets/<id>` | Update an existing asset |
| DELETE | `/assets/<id>` | Delete an asset |

## Authentication Examples

### Register a user

**POST `/signup`**

Request body:

```json
{
  "username": "artist01",
  "password": "Password123!",
  "password_confirmation": "Password123!"
}
```

### Log in

**POST `/login`**

Request body:

```json
{
  "username": "artist01",
  "password": "Password123!"
}
```

A successful response returns a JWT token and user information.

### Access a protected endpoint

Include the token in the request header:

```text
Authorization: Bearer YOUR_JWT_TOKEN
```

### Retrieve the authenticated user

**GET `/me`**

Example response:

```json
{
  "id": 1,
  "username": "artist01"
}
```

## Asset Management Examples

### Create an asset

**POST `/assets`**

Request body:

```json
{
  "name": "Sci-Fi Character",
  "description": "A custom futuristic 3D character model.",
  "category": "character",
  "format": "BLEND"
}
```

### Retrieve assets

**GET `/assets?page=1&per_page=10`**

The response includes the assets, total number of records, page number, and pagination information.

### Update an asset

**PATCH `/assets/1`**

Request body:

```json
{
  "name": "Updated Sci-Fi Character"
}
```

### Delete an asset

**DELETE `/assets/1`**

A successful deletion returns HTTP status `204 No Content`.

## Security and Access Control

- Passwords are hashed using Flask-Bcrypt rather than stored as plain text.
- JWT authentication protects private API routes.
- Each asset is associated with its creator through `user_id`.
- Users can only retrieve, modify, and delete their own assets.
- Attempts to access another user's asset return HTTP `404 Not Found`.

## Running Tests

Run the automated test suite from the backend directory:

```bash
pipenv run pytest -v
```

The test suite covers:

- User registration
- Duplicate username prevention
- User login
- Authentication requirements
- Asset creation and retrieval
- Asset updates and deletion
- User ownership restrictions

Tests use an isolated in-memory SQLite database and do not modify the development database.

## License

This project was developed as part of a Moringa School summative lab.
