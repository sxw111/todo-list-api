# Async Todo List Project using FastAPI

This project is an asynchronous todo list application built using FastAPI, a modern web framework for building APIs with Python.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete tasks.
- **Asynchronous**: Utilizes asynchronous programming to handle concurrent requests efficiently.
- **RESTful API**: Implements a RESTful API architecture for managing todo tasks.
- **Swagger Documentation**: Automatically generated API documentation using Swagger UI.
- **PostgreSQL Database**: Uses PostgreSQL for storing task data.
- **Fast**: Built on FastAPI, leveraging the performance benefits of Python's async capabilities.

## Technologies

- Python 3.10+
- FastAPI
- Uvicorn (ASGI server)
- SQLAlchemy with async support
- Alembic for migrations
- Asynchronous PostgreSQL
- Docker and docker-compose

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/todo-list-api.git
   cd todo-list-api
   ```

2. Build and Run the Docker Containers:
   
   ```bash
   docker-compose up --build
   ```

3. Open your browser and go to http://localhost:8000/docs to view the Swagger documentation and interact with the API.

## Project Structure

```shell
.vscode/
├── settings.json                       # VSCode settings
app/
├── api/
    ├── routers/
        ├── auth.py                     # Authentication router
        ├── todos.py                    # Todos router
        ├── users.py                    # Users router
    deps.py                             # Application dependencies
    endpoints.py                        # Endpoint registration
├── core/
    ├── config.py                       # Application configuration
    ├── db.py                           # Database configuration
    ├── security.py                     # Security configuration
├── crud
    ├── todo.py                         # Todo CRUD operations
    ├── user.py                         # User CRUD operations
├── models
    ├── db/
        ├── todo.py                     # Todo SQLAlchemy Model
        ├── user.py                     # User SQLAlchemy Model
    ├── schemas/
        ├── jwt_token.py                # JWT token Pydantic schemas
        ├── todo.py                     # Todo Pydantic schemas
        ├── user.py                     # User Pydantic schemas
├── utilities
    ├── exceptions/
        ├── http/
            ├── exc_400.py              # Custom 400 errors
            ├── exc_401.py              # Custom 401 errors
            ├── exc_403.py              # Custom 403 errors
            ├── exc_404.py              # Custom 404 errors
        ├── access.py                   # Custom Exception class
        ├── database.py                 # Custom Exception class
        ├── password.py                 # Custom Exception class 
    ├── messages/
        ├── exc_details.py              # Custom message for HTTP exceptions
├── main.py                             # FastAPI application setup
migrations/                             # Alembic migrations
tests/
.dockerignore                           # Excludes unnecessary files and directories from Docker image builds
.env                                    # File for storing sensitive environment variables
.flake8                                 # Configuration file for Flake8 code linter
.gitattributes                          # Configuration file for specifying attributes for Git repositories
.gitignore                              # File specifying files and directories Git should ignore
Dockerfile                              # Script defining steps to create a Docker image
LICENSE                                 # File containing terms and conditions for software usage and distribution
README.md                               # Project overview and instructions for users and developers
alembic.ini                             # Configuration file for Alembic database migrations
docker-compose.yml                      # Configuration file for Docker Compose
poetry.lock                             # Automatically generated file containing locked dependencies for Poetry
pyproject.toml                          # Configuration file for Python projects, specifying project metadata and dependencies
```

## Contributing

Your contributions are appreciated! Fork the repository, open issues, and submit pull requests.