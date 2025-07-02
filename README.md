# Apithon Custom API Testing Framework

## Overview

The Apithon Custom API Testing Framework is a Python-based solution tailored for efficient and comprehensive testing of APIs. It emphasizes ease of integration, adaptability, and thorough testing coverage, making it ideal for ensuring the reliability and performance of your API services.

## Core Components

### `api_clients/`

This directory houses the Python modules that abstract the API endpoints being tested. These client modules are responsible for sending requests to the APIs and receiving responses. They play a crucial role in encapsulating the logic for API interaction, making the tests cleaner and more maintainable.

### `environment_data/`

Contains configuration files and data sets used to define different testing environments. This may include base URLs, authentication credentials, and any other environment-specific settings that are necessary to execute the tests across various stages (development, testing, staging, production).

### `resources/`

A repository for additional files that tests may require, such as JSON schemas for response validation, sample request payloads, and expected response data. This directory helps in organizing resources that support test assertions and data-driven testing.

### `tests/`

The core of the framework, where all test cases are defined. This directory is structured to reflect the API's structure, with subdirectories for different services or resource types. It includes:

- **`tests.api_tests/`**: Contains test modules for each API endpoint, organized by service.

## Getting Started

### Prerequisites

- Ensure you have Python 3.x installed on your system. The framework is designed to be compatible with modern Python versions.
- And you are comfortable to use command line tools like `Terminal` for example on Mac and `Command Prompt` on Windows.

#### Basic setup and installation
- install python 3.12 (install for local user only works; win: use the Windows AppStore)
- figure out where your system thinks your python 3 lives: `python --version`
  - if this returns something like `Python 3.12.2`, python 3 is your default python version
  - if this return something else, check if `python3 --version` returns something like `Python 3.12.2`
  - if `python3 --version` also returns something else, something has gone wrong in an interesting way
- Make sure you have git installed on your machine.
- clone this repository `git clone https://github.com/gaurav-sancheti/apithon/tree/main`
- go into the repository directory
- create a virtual environment named `venv`:
  - if python 3 is your default python: `python -m venv venv`
  - if it isn't: `python3 -m venv venv`
- activate the virtual environment: mac/linux: `source venv/bin/activate`, win: `venv\Scripts\activate` (CMD.exe and Powershell.exe supported)
- install necessary libraries: `pip install -r requirements.txt`

When you're done executing the tests, deactivate the virtual environment by typing `deactivate`.

#### Some explanations on the above instructions
- Mac and linux come with Python 2 installed as part of the OS; Windows does not. So for the former you'll likely have to use the `python3` thing, for Windows not.
- Virtual environments allow you to create an isolated python environment in which you install repo-specific libraries. It's better than the alternative of dependency hell.


#### Setting up a pre-commit hook
If you want to run `flake8` (linting tool) automatically before every commit, you can set up a git pre-commit hook:
1. install the [pre-commit framework](https://pre-commit.com/#install)
1. include [flake8 as a pre-commit hook](https://flake8.pycqa.org/en/latest/user/using-hooks.html#usage-with-the-pre-commit-git-hooks-framework)
1. run `pre-commit install` to install the flake8 pre-commit hook

Note that running the hook for the very first time may take some time, because it will download and install the hook.

## Running tests with pytests
The API tests can be run with pytest. You can do this from the command line or from Pycharm.

### Running from the command line
`pytest [command line arguments] [path to tests you want to run]`

If you omit the path, pytest will collect all tests in the current directory and its sub-directories.

Command line arguments: 
- `--env { test | accp | local_{app_name} | docker }`: determines which environment data file to load. Defaults to `None`.
- `--random-order`: runs tests in a random order; for more options see https://pypi.org/project/pytest-random-order/.

Examples
* company service example: `pytest --env test --random-order tests/api_tests/company_service/`

To see a list of tests in a directory or module, use `--collect-only -q`.
For more command-line options, see https://docs.pytest.org/en/latest/usage.html


### Running with Pycharm
To run tests from within Pycharm:
- File > Settings > Project > Project Interpreter: set to your virtual environment
- File > Settings > Tools > Python Integrated Tools: set Default test runner to pytest
- Run > Edit Configurations...
    - go to Templates > Python tests > pytest
    - Additional arguments: add `--env <env>`
    - Python interpreter: select your virtual environment
    - Working directory: set to root of repository

## Testing Strategy

The framework adopts a structured approach to API testing, encouraging clear separation of concerns and reusability:

- **Modular Design**: Organizes tests by service and functionality, allowing for targeted testing and easier maintenance.
- **Data-Driven Testing**: Leverages `environment_data` and `resources` to parameterize tests, facilitating comprehensive test coverage across different scenarios.
- **Extensibility**: Designed to easily accommodate new tests and resources as your API evolves.


## Running performance tests with Locust.io
- Make sure to install locust on your machine like for example `pip install locust`
- WebUI: `locust -f tests/performance_tests/company_service/company_service_odata_api.py`  
- WebUI is available at http://0.0.0.0:8089/ (on Mac) or maybe something like http://127.0.0.1:8089/ (on Windows) after running locust on the command-line     
- CLI: `locust -f tests/performance_tests/company_service/company_service_odata_api.py --headless --users 1000 --spawn-rate 100 --run-time 10m`


## Additional resources
- Pytest docs: https://docs.pytest.org/en/latest/contents.html
- Pytest API reference: https://docs.pytest.org/en/latest/reference.html
- Requests library: https://requests.kennethreitz.org/en/master/
- Python Selenium API docs: http://selenium-python.readthedocs.io/api.html
- JSON schema: https://json-schema.org/understanding-json-schema/
- XML schema: https://xmlschema.readthedocs.io/en/latest/index.html
- Schema library: https://pypi.org/project/schema/
- Locust.io: https://locust.io/

