# Playwright Automation Framework (Python + Pytest-BDD)

## Project Overview
This repository contains a web automation framework built using:
- Playwright (Python) for browser automation
- Pytest + Pytest-BDD for test execution and BDD-style scenarios
- Allure for execution reporting

Current coverage includes login, signup, and forgot-password flows.

## Prerequisites
Install the following on your machine:
- Python 3.9+ (3.10/3.11 also fine)
- Git
- VS Code
- Java 8+ (required for Allure CLI)
- Allure CLI

## Mac Setup (A to Z)
Follow these steps in order.

1. Install Homebrew (if not installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Python, Git, Java, and Allure:
```bash
brew install python git openjdk allure
```

3. Verify installations:
```bash
python3 --version
pip3 --version
git --version
java -version
allure --version
```

4. Install VS Code from:
- https://code.visualstudio.com/

5. Install recommended VS Code extensions:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- GitLens (eamodio.gitlens) (optional)
- Markdown All in One (yzhang.markdown-all-in-one) (optional)

6. Configure Git identity (first-time only):
```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

7. Clone repo and open it:
```bash
git clone <your-repo-url>
cd Repcard-Automation
code .
```

8. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

9. Install framework dependencies:
```bash
pip install -r requirements.txt
```

10. Install Playwright browser binaries:
```bash
playwright install
```

11. Run tests:
```bash
HEADLESS=1 pytest --env=qa
```

12. Generate and open Allure report:
```bash
pytest --env=qa --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## Windows Setup (A to Z)
Follow these steps in order (PowerShell).

1. Install Python:
- Download from https://www.python.org/downloads/windows/
- During install, check "Add Python to PATH"

2. Install Git:
- Download from https://git-scm.com/download/win

3. Install VS Code:
- Download from https://code.visualstudio.com/

4. Install Java:
- Use Temurin/OpenJDK (example): https://adoptium.net/

5. Install Allure CLI (choose one):
```powershell
choco install allure-commandline
```
or
```powershell
scoop install allure
```

6. Verify installations:
```powershell
python --version
pip --version
git --version
java -version
allure --version
```

7. Install recommended VS Code extensions:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- GitLens (eamodio.gitlens) (optional)
- Markdown All in One (yzhang.markdown-all-in-one) (optional)

8. Configure Git identity (first-time only):
```powershell
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

9. Clone repo and open it:
```powershell
git clone <your-repo-url>
cd Repcard-Automation
code .
```

10. Create and activate virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

11. Install framework dependencies:
```powershell
pip install -r requirements.txt
```

12. Install Playwright browser binaries:
```powershell
playwright install
```

13. Run tests:
```powershell
$env:HEADLESS="1"
pytest --env=qa
```

14. Generate and open Allure report:
```powershell
pytest --env=qa --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## Framework Commands
Run all tests:
```bash
pytest --env=qa
```

Run login tests only:
```bash
pytest tests/web/test_userlogin.py --env=qa
```

Run signup tests only:
```bash
pytest tests/web/test_signup.py --env=qa
```

Run forgot-password tests only:
```bash
pytest tests/web/test_forgot_password.py --env=qa
```

## Common Troubleshooting
Playwright browser not found:
```bash
playwright install
```

Allure command not found:
- Reinstall Allure and restart terminal.

Allure report opens but shows blank/404:
- Always use `allure open reports/allure-report` or `allure serve reports/allure-results`.
- Avoid opening `index.html` directly from file path.

QA environment unstable/down:
- Tests may fail due to backend issues; rerun after environment recovery.
