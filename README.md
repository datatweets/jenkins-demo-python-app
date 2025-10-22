# Jenkins Demo Python App

A sample Python application demonstrating CI/CD pipeline with Jenkins on Google Colab using virtual environments.

## Features

- Python virtual environment (.venv) isolation
- Unit testing with pytest
- Code coverage reporting
- Code quality analysis with pylint
- Security scanning with bandit
- Code formatting check with black
- Distribution packages (sdist, wheel)
- Jenkins CI/CD integration
- Multi-environment deployment (dev, staging, prod)

## Project Structure

```text
.
|-- src/
|   +-- app.py                 # Main application
|-- tests/
|   +-- test_app.py            # Unit tests
|-- scripts/
|   |-- deploy-dev.sh          # Dev deployment script
|   |-- deploy-staging.sh      # Staging deployment script
|   +-- deploy-prod.sh         # Production deployment script
|-- build/
|   +-- artifacts/             # Build output (generated)
|-- .venv/                     # Virtual environment (generated)
|-- Jenkinsfile                # Jenkins pipeline definition
|-- requirements.txt           # Python dependencies
|-- setup.py                   # Package setup
|-- pytest.ini                 # Pytest configuration
|-- .pylintrc                  # Pylint configuration
|-- .gitignore                 # Git ignore patterns
|-- tutorial.md                # Jenkins setup tutorial
+-- README.md                  # This file
```

## Quick Start

For detailed setup instructions, see [tutorial.md](tutorial.md) which includes:

- How to set up Jenkins with GitHub integration
- Configuring pipeline parameters
- Running your first build
- Accessing build reports and artifacts
- Jenkins CLI commands

## Local Development Setup

```bash
# Clone repository
git clone https://github.com/datatweets/jenkins-demo-python-app.git
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
python src/app.py

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

See [tutorial.md](tutorial.md) for complete step-by-step instructions on:

1. Setting up GitHub Personal Access Token
2. Creating Jenkins Pipeline job
3. Configuring job parameters (BRANCH, ENVIRONMENT)
4. Connecting Jenkins to GitHub repository
5. Running builds via UI or CLI
6. Accessing build results and artifacts

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

## Accessing Build Reports & Artifacts

After a successful Jenkins build, you can access various reports and artifacts:

### How to Access Reports

1. **Go to your Jenkins build page**: `http://your-jenkins-url/job/jenkins-demo-python-app/[BUILD_NUMBER]/`
2. **Navigate to different sections**:

#### Test Reports
- Click **"Test Result"** in the left sidebar
- View detailed test results, trends, and failure reports
- URL: `[BUILD_URL]/testReport/`

#### Build Artifacts
- Click **"Build Artifacts"** in the left sidebar  
- Download or view all generated files
- URL: `[BUILD_URL]/artifact/`

#### Coverage Reports
- Go to **Build Artifacts** → `build/artifacts/htmlcov/`
- Click on `index.html` to view interactive coverage report
- Shows line-by-line coverage with color coding

#### Security Scan Results  
- Go to **Build Artifacts** → `build/artifacts/`
- Download `bandit-report.json` for detailed security analysis

#### Console Output
- Click **"Console Output"** to see full build logs
- URL: `[BUILD_URL]/console`

### Build Artifacts Generated

| File/Directory | Purpose |
|----------------|---------|
| `test-results.xml` | JUnit format test results for Jenkins integration |
| `coverage.xml` | Code coverage in XML format |
| `htmlcov/index.html` | **Interactive HTML coverage report** |
| `bandit-report.json` | Security scan results (JSON format) |
| `build-info.txt` | Build metadata (build number, commit, author) |
| `*.tar.gz` | Source distribution package |
| `*.whl` | Wheel distribution package |

### Quick Access Tips

- **Bookmark your Jenkins job**: `http://your-jenkins-url/job/jenkins-demo-python-app/`
- **Latest build**: Add `/lastBuild/` to quickly access the most recent build
- **Coverage trends**: Jenkins tracks coverage over time in the main job page
- **Build history**: Click on build numbers in the left sidebar for historical builds

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

## Pipeline Configuration

### Environment Variables

The pipeline uses the following environment variable:

- `PYTHONPATH` = `${WORKSPACE}/src`

### Virtual Environment Paths

The pipeline creates and uses `.venv` in the workspace:

- Virtual environment directory: `${WORKSPACE}/.venv`
- Virtual environment binaries: `${WORKSPACE}/.venv/bin`
- Activation: `. .venv/bin/activate`

All tools (pytest, pylint, black, bandit) are executed within the activated virtual environment.

## Key Changes from Original

### Removed Dependencies on External URLs

- No hardcoded Jenkins URLs (uses Jenkins built-in `${BUILD_URL}` variable)
- Removed ngrok-specific configuration
- Works with any Jenkins instance

### Simplified Virtual Environment Handling

- Uses relative paths (`.venv/bin/activate` instead of `${VENV_BIN}/activate`)
- More robust Python detection with fallback
- Handles missing `ensurepip` gracefully

### Clean Output

- All emoji characters removed from pipeline output
- Professional, system-compatible text messages
- Better error messages with clear prefixes (ERROR, WARNING)

## License

MIT
