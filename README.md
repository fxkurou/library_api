![Django CI](https://github.com/Maze-Logic/seek-event-backend/workflows/Django%20CI/badge.svg)
# Library. Backend 🎉

## Description
This is a backend for the Library project. It is a REST API that provides endpoints to manage events and users.

## Technologies
- Django 🐍
- Django REST Framework 🌐
- PostgreSQL 🗃️
- Docker 🐳
- Docker Compose 🧩
- Redis 🚀
- Celery 🌿

## Docker Installation 🐳
To set up the project using Docker, follow these steps:
1. Clone the repository
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Create a `.env` file in the root directory with the following content as in the `.env.example` file
3. Run
    ```sh
       docker-compose up
    ```
4. Access the API at `http://localhost:8000/api/`

## Local Installation 💻
For a local setup without Docker, perform the following steps:
1. Clone the repository
   ```sh
      git clone <repository-url>
      cd <repository-directory>
      ```
2. Install Poetry if you don't have it installed
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Install dependencies
   ```sh
    poetry install
    ```
4. Create a `.env` file in the root directory with the following content as in the `.env.example` file
5. Apply migrations
    ```sh
    poetry run python manage.py migrate
    ```
6. Start the server
    ```sh
    poetry run python manage.py runserver
    ```
7. Access the API at `http://localhost:8000/api/`

## Pre-Commit Hooks Installation ✅
Ensure your code quality by setting up pre-commit hooks:
1. Install pre-commit
    ```sh
    poetry run pre-commit install
    ```
2. Run pre-commit hooks
    ```sh
    poetry run pre-commit run --all-files
    ```

## Coverage Report 📊
To generate a coverage report, run the following command:
```sh
poetry run coverage run --source='.' manage.py test
poetry run coverage report
```

If you want to generate an XML report, run:
```sh
poetry run coverage xml
```

If you want to generate an HTML report, run:
```sh
poetry run coverage html
```


## Commitzen 📝
To make commits easier, we use Commitizen. To make a commit, run:
```sh
poetry run cz commit
```

If you have already not installed Commitizen, run:
```sh
poetry run commitzen install
poetry run pre-commit install --hook-type commit-msg --hook-type pre-push
```
