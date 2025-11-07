# automationexercise

# Automation Exercise Tests

![Python](https://img.shields.io/badge/python-3.10%2B-blue)

This repository contains automated tests for the Automation Exercise web application. It uses #MITÄ together with the #MITÄ to run tests against the test environment. 

# Setup environment
## Virtual environment
Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment on Windows

```bash
venv\Scripts\activate
```
Activate virtual environment on Linux / macOS 
```bash
source venv/bin/activate
```

## Dependencies
Install dependencies from `requirements.txt` ä

```bash
pip install -r requirements.txt
```

# Secrets for login and api key are stored in .env 
# PITÄÄ MUOKATA! TÄÄ ON KOPIOITU VIBECATCHISTA
Create a file named .env in your local project-root folder and replace <YOUR_USERNAME> and <YOUR_PASSWORD> with your personal login credentials.
```
USER=<YOUR_USERNAME>
PASSWORD=<YOUR_PASSWORD>
POLL_API=api/v1/feedbacks?apiKey=<YOUR_API_KEY>
```

# Running tests locally

Run all tests using command

```bash
# tähän command
```
📂 Test results will be saved in the results/ folder.

Run all tests with tag 'smoke' using command

```bash
# tähän command
```

### Tags 
Currently used tags in the repository:
