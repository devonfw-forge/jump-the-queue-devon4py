# JUMP THE QUEUE

In this section you will find an overview on how to execute and configure the project.

## Dependencies
Dependencies are automatically managed by **Poetry**

To install dependencies run
```bash
poetry install
```
In same folder where your `.toml` file is located. 
Poetry will take care of:
- Installing the required Python interpreter 
- Installing all the libraries and modules 
- Creating the virtual environment for you

Refer to [this link](https://www.jetbrains.com/help/pycharm/poetry.html) to configure Poetry on PyCharm

## Running on local

You can launch the uvicorn server programmatically running directly the main.py file.

```shell
python main.py
```

It is also possible to start the uvicorn live directly server with the command:

```shell
uvicorn main:api --reload
```

- **_main_**: the file main.py (the Python "module").
- **_app_**: the object created inside of main.py with the line app = FastAPI().
- _**--reload**_: make the server restart after code changes. Only use for development.

## Run Tests with coverage
You can run all test scenarios using:
```
python -m coverage run -m unittest
```

To display the coverage results:

```
coverage report
```

or with a nicer report as html page:

```
coverage html
```

