# Jenkins Demo Python App

A sample Python application demonstrating CI/CD pipeline with Jenkins on Google Colab using virtual environments.

## Features

- ✅ Python virtual environment (.venv) isolation
- ✅ Unit testing with pytest
- ✅ Code coverage reporting
- ✅ Code quality analysis with pylint
- ✅ Security scanning with bandit
- ✅ Code formatting check with black
- ✅ Distribution packages (sdist, wheel)
- ✅ Jenkins CI/CD integration
- ✅ Multi-environment deployment (dev, staging, prod)

## Project Structure
```
.
├── src/
│   └── app.py                 # Main application
├── tests/
│   └── test_app.py            # Unit tests
├── scripts/
│   ├── deploy-dev.sh          # Dev deployment script
│   ├── deploy-staging.sh      # Staging deployment script
│   └── deploy-prod.sh         # Production deployment script
├── build/
│   └── artifacts/             # Build output (generated)
├── .venv/                     # Virtual environment (generated)
├── Jenkinsfile                # Jenkins pipeline definition
├── requirements.txt           # Python dependencies
├── setup.py                   # Package setup
├── pytest.ini                 # Pytest configuration
├── .pylintrc                  # Pylint configuration
├── .gitignore                 # Git ignore patterns
└── README.md                  # This file
```

## Local Development Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/jenkins-demo-python-app.git
cd jenkins-demo-python-app

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list

# Run tests
pytest tests/ -v

# Run the application
python3 src/app.py

# Run linting
pylint src/app.py

# Run security scan
bandit -r src/

# Format code
black src/ tests/

# Deactivate virtual environment when done
deactivate
```

## Virtual Environment (.venv) Usage

### What is .venv?

`.venv` is a Python virtual environment that isolates project dependencies. Each project has its own `.venv` folder containing:
- Python interpreter
- pip package manager
- Installed packages (from requirements.txt)

### Why use .venv?

1. **Isolation**: Keeps project dependencies separate from system Python
2. **Reproducibility**: Same versions across different machines
3. **Clean builds**: Fresh environment for CI/CD pipelines
4. **No conflicts**: Multiple projects can use different versions of packages

### Important: .venv is NOT committed to Git

The `.gitignore` file excludes `.venv/` so it won't be pushed to GitHub. Instead:
- Commit only `requirements.txt`
- CI/CD pipeline recreates `.venv` automatically
- Each developer creates their own `.venv` locally

## Jenkins Pipeline Stages with .venv

1. **Checkout** - Clone repository and extract commit info
2. **Create Virtual Environment** - Creates or reuses `.venv`
3. **Install Dependencies** - Installs packages from `requirements.txt` into `.venv`
4. **Code Quality** - Run pylint from `.venv`
5. **Code Formatting** - Check code style with black from `.venv`
6. **Unit Tests** - Execute pytest from `.venv` with coverage
7. **Build Artifacts** - Create distribution packages using `.venv`
8. **Security Scan** - Run bandit from `.venv`
9. **Deploy** - Deploy to selected environment
10. **Health Check** - Verify application health
11. **Cleanup** - Purge pip cache in `.venv`

## Jenkins Setup

1. Create a new Pipeline job in Jenkins
2. Configure SCM to point to this repository
3. Set pipeline script path to `Jenkinsfile`
4. Configure GitHub credentials with personal access token
5. Build with parameters (BRANCH and ENVIRONMENT)

## Managing Dependencies

### Add a new package
```bash
# Activate .venv
source .venv/bin/activate

# Install package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Commit changes
git add requirements.txt
git commit -m "Add new dependency: package-name"
git push origin main
```

### Update all packages
```bash
source .venv/bin/activate
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

## Build Artifacts Generated

| File | Purpose |
|------|---------|
| `test-results.xml` | JUnit format test results |
| `coverage.xml` | Code coverage in XML format |
| `htmlcov/` | Interactive HTML coverage report |
| `bandit-report.json` | Security scan results |
| `pylint-report.txt` | Code quality analysis |
| `*.tar.gz` | Source distribution package |
| `*.whl` | Wheel distribution package |
| `source.tar.gz` | Complete source code archive |

## Build Pipeline Triggers

### Via Jenkins UI
1. Click "Build with Parameters"
2. Select BRANCH (default: main)
3. Select ENVIRONMENT (dev/staging/prod)
4. Click "Build"

### Via Jenkins CLI
```bash
java -jar jenkins-cli.jar -s https://your-jenkins-url/ \
  -auth username:token \
  -noCertificateCheck build jenkins-demo-python-app \
  -p BRANCH=main \
  -p ENVIRONMENT=dev
```

## Environment Variables in Pipeline

- `VENV_DIR` = `${WORKSPACE}/.venv`
- `VENV_BIN` = `${WORKSPACE}/.venv/bin`
- `PYTHONPATH` = `${WORKSPACE}/src:${PYTHONPATH}`

All tools (pytest, pylint, black, bandit) are run using `. ${VENV_BIN}/activate`

## License

MIT
