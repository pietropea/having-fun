# Backend component of the Having Fun tool

## Local development
```
cd ./api
source .venv/bin/activate
uvicorn app.main:app --reload
```

### API doc

````

http://127.0.0.1:8000/docs 

````

https://medium.com/@julgq/how-to-deploy-fastapi-on-heroku-using-github-4363d9ba3d41

## Development features

These features are implemented for the project:
- Github actions configuration form:
  - Code formatting and linting ([black](https://pypi.org/project/black/))
  - Strict type checking ([mypy](https://pypi.org/project/mypy/))
  - Static code analysis ([bandit](https://pypi.org/project/bandit/))
  - Dependencies security checks ([safety](https://pypi.org/project/safety/))
- Testing ([pytest](https://pypi.org/project/pytest/))
- Pre-commit hook configuration for code formatting and linting.
- Visual studio configuration for code formatting and linting.

## Getting started

Before start coding, please run the following command from the project root folder to install the project dependencies and the pre-commit hook:

```
$ ./scripts/bootstrap.sh
```

and then activate the python virtual environment with:

```
$ source .venv/bin/activate
```

and happy coding!