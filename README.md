# Automation Exercise Tests

![Logo](docs/logo.jpg)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)

![License](https://img.shields.io/badge/license-MIT-blue)

![Robot Framework](https://img.shields.io/badge/robot--framework-7.1-green)

This repository contains automated tests for the Automation Exercise web application. It uses #MITÄ together with the #MITÄ to run tests against the test environment. 

# Setup environment
## Virtual environment
Create virtual environment

```
python -m venv venv
```

Activate virtual environment on Windows

```
venv\Scripts\activate
```
Activate virtual environment on Linux / macOS 
```
source venv/bin/activate
```

Install dependencies from `requirements.txt` 

```
pip install -r requirements.txt
```

Then run

````
rfbrowser init
````

# Secrets for login and api key are stored in .env 
# PITÄÄ MUOKATA! TÄÄ ON KOPIOITU VIBECATCHISTA
Create a file named .env in your local project-root folder and replace <YOUR_USERNAME> and <YOUR_PASSWORD> with your personal login credentials.
```
USER=<YOUR_USERNAME>
PASSWORD=<YOUR_PASSWORD>
POLL_API=api/v1/feedbacks?apiKey=<YOUR_API_KEY>
```

# Running tests locally

Run tests with command
````
robot -d results ADD_YOUR_TEST_NAME_HERE
````

````
📂 Test results will be saved in the results/ folder.
````
Run all tests with tag 'smoke' using command

```bash
# tähän command
```

### Tags 
Currently used tags in the repository:
