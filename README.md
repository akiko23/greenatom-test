# Greenatom-test

Greenatom test task


## 🛠 Installation and Usage

1. Clone the project & enter its directory
   ```
   git clone https://github.com/akiko23/greenatom-test
   cd greenatom-test
   ```

2. Initialise and activate virtual environment (Its supposed that you have preinstalled python and python-virtualenv)
    ```
    python -m venv venv
    .\venv\Scripts\activate
    ```

3. Install dependencies & distributable package
   ```
   pip install .
   ```

   #### [Optional]
   3.1. Install dev dependencies
   ```
   pip install .[dev]
   ```

   3.2. Run tests
   ```
   pytest .\tests\unit
   pytest .\tests\integration 
   ```

   3.3. Run linters
   ```
   mypy -p src -v --follow-imports=normal
   isort .
   ruff . --fix
   ```

4. Rename **app.example.toml** to **app.toml** or create your own

5. Run the database migrations
   ```
   alembic upgrade head
   ```

6. Run the application
   ```
   python -m src.greenatom_task
   ```

7. Check the docs in your browser: <a href="http://localhost:8000/docs">click</a>

## 🧰 Tech Stack

### Web API

- [FastAPI](https://fastapi.tiangolo.com/) - Modern and fast python web-framework for building APIs;

### Backend/low-level part

- [Pydantic](https://docs.pydantic.dev/latest/) - A most popular library for building validation rules;
- [SQLAlchemy](https://www.sqlalchemy.org/) - An ORM and SQL toolkit that provides easy database interaction from
  python;
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Database migration tool for SQLAlchemy.

### Testing

- [Pytest](https://docs.pytest.org) - A python testing framework;
- [Unittest](https://docs.python.org/3/library/unittest.html) - A python builtin library for building unit tests

### Docs

- [SwaggerUI](https://github.com/swagger-api/swagger-ui) - A tool for describing, visualizing and interaction with the
  API’s resources

## Versioning

The [SemVer](http://semver.org/) is used for versioning. For the versions available, see
the [tags on this repository](https://github.com/akiko23/greenatom-test/tags).

## Authors

> See the list of [contributors](https://github.com/akiko23/greenatom-test/graphs/contributors) who participated in this
> project.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details

