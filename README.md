# API-Testing-for-Fun-and-Profit_2

### Python version and installation

Tests are written in Python 3.8+ and it should be ran on this version or higher.
User can download newest version of Python at [Python download site](https://www.python.org/downloads/).

Install [PIP](https://pypi.org/project/pip/).

### Installing required packages and tools

After cloning [API Testing for Fun and Profit](https://github.com/PyShaman/API-Testing-for-Fun-and-Profit.git) repository locally user should enter
repository folder and create separate virtual environment for this project by using following command:
```
$ python -m venv venv
```
Python will create new directory called venv and install there basic packages. Next step is to activate virtual environment:
```
PS > ./venv/Scripts/Activate.ps1
```
for Windows systems or
```
$ ./venv/Scripts/activate
```
for Linux.
When virtual environment will be activated the user will see additional mark at console:
```
(venv) path\API-Testing-for-Fun-and-Profit >
```
Next step is to install required packages using following command:
```
PS > pip install -r requirements.txt
```
for Windows systems or
```
$ pip3 install -r requirements.txt
```
for Linux.

This will automatically download and install all necessary packages.

### Usage:

To run all tests use following command:
```
$ pytest -v -s
```

### Output:

The tests will perform API tests for non-existing endpoints.

### Generating Allure Reports

To generate Allure Reports please follow [installation guide](https://docs.qameta.io/allure/#_installing_a_commandline).

To initiate Allure Listener use following command:
```
$ pytest --alluredir=/tmp/my_allure_results
```
To see actual report use following command:
```
$ allure serve /tmp/my_allure_results
```

### Reproduce swagger.yml file

To reproduce swagger.yml file copy and paste content of file in the following [Swagger Editor](https://editor.swagger.io/)