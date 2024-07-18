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

2. Build the Docker image:
   
   ```bash
   docker build -t todo-list-api .
   ```

3. Run the Docker container:
   
   ```bash
   docker run -d -p 8000:8000 todo-list-api
   ```

4. Open your browser and go to http://localhost:8000/docs to view the Swagger documentation and interact with the API.

## Project Structure

```shell
.vscode/
app/
├── api/
    ├── routers/
        ├── auth.py
        ├── todos.py
        ├── users.py
    deps.py
    endpoints.py
├── core/
    ├── config.py
    ├── db.py
    ├── security.py
├── crud
    ├── todo.py
    ├── user.py
├── models
    ├── db/
        ├── todo.py
        ├── user.py
    ├── schemas/
        ├── jwt_token.py
        ├── todo.py
        ├── user.py
├── utilities
    ├── exceptions/
        ├── http/
            ├── exc_400.py
            ├── exc_401.py
            ├── exc_403.py
            ├── exc_404.py
        ├── access.py
        ├── database.py
        ├── password.py
    ├── messages/
        ├── exc_details.py
├── main.py
migrations/
tests/
.dockerignore
.env
.flake8
.gitattributes
.gitignore
Dockerfile
LICENSE
README.md
alembic.ini
docker-compose.yml
poetry.lock
pyproject.toml
```

## Contributing

Your contributions are appreciated! Fork the repository, open issues, and submit pull requests.