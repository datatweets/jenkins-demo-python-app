# Jenkinsfile Tutorial: Complete Guide

## Table of Contents

- [What is a Jenkinsfile?](#what-is-a-jenkinsfile)
- [Why Do We Need a Jenkinsfile?](#why-do-we-need-a-jenkinsfile)
- [Pipeline as Code Benefits](#pipeline-as-code-benefits)
- [Jenkinsfile Syntax](#jenkinsfile-syntax)
- [Creating Your First Jenkinsfile](#creating-your-first-jenkinsfile)
- [Understanding Our Jenkinsfile](#understanding-our-jenkinsfile)
- [Step-by-Step Breakdown](#step-by-step-breakdown)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## What is a Jenkinsfile?

A **Jenkinsfile** is a text file that contains the definition of a Jenkins Pipeline. It's written using a Groovy-based DSL (Domain Specific Language) and is stored in your source code repository alongside your application code.

### Key Characteristics

- **Text-based**: Written in Groovy DSL
- **Version-controlled**: Stored in Git with your code
- **Declarative or Scripted**: Two syntax options
- **Self-documenting**: Pipeline definition is code

---

## Why Do We Need a Jenkinsfile?

### 1. Version Control for CI/CD

Just like your application code, your CI/CD pipeline should be versioned:

```text
Before Jenkinsfile:
- Pipeline configuration in Jenkins UI
- No history of changes
- Hard to replicate
- Manual setup for each project

With Jenkinsfile:
- Pipeline definition in Git
- Full change history
- Easy to replicate
- Automated setup
```

### 2. Code Review for Pipelines

You can review pipeline changes just like code changes:

```bash
git diff Jenkinsfile
# See exactly what changed in your build process
```

### 3. Single Source of Truth

Everything needed to build your project is in the repository:

```text
Repository Contents:
├── src/              # Application code
├── tests/            # Test code
├── Jenkinsfile       # Build instructions
└── README.md         # Documentation
```

### 4. Disaster Recovery

If Jenkins server crashes, you don't lose your pipeline definitions:

- Clone repository
- Set up new Jenkins
- Point to repository
- Pipeline automatically restored

---

## Pipeline as Code Benefits

### Consistency

```groovy
// Same build process everywhere
pipeline {
    // Runs identically on:
    // - Developer's local Jenkins
    // - CI/CD server
    // - Production Jenkins
}
```

### Reusability

```groovy
// Share pipeline code across projects
@Library('shared-pipeline-library') _
```

### Auditability

```bash
# Who changed the build process?
git log Jenkinsfile

# What changed?
git show commit-hash
```

---

## Jenkinsfile Syntax

Jenkins supports two types of syntax:

### 1. Declarative Pipeline (Recommended)

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
    }
}
```

**Pros:**

- Easier to read and write
- More structured
- Better error messages
- Validation support

### 2. Scripted Pipeline (Advanced)

```groovy
node {
    stage('Build') {
        echo 'Building...'
    }
}
```

**Pros:**

- More flexibility
- Full Groovy power
- Complex logic easier

**Our project uses Declarative Pipeline** for better readability and maintainability.

---

## Creating Your First Declarative Pipeline

### Step 1: Basic Structure (Sample Jenkinsfile)

```groovy
pipeline {
    agent any
    
    stages {
        stage('Hello') {
            steps {
                echo 'Hello World!'
            }
        }
    }
}
```

### Step 2: Create Test Pipeline Job

1. In Jenkins, click **"New Item"**
2. Enter name: `test-pipeline`
3. Select **"Pipeline"**
4. Under **Pipeline** section, select **"Pipeline script"**
5. Paste your Jenkinsfile content
6. Click **"Save"**
7. Click **"Build Now"** to test

**This method lets you:**

- See real-time console output
- Test Groovy syntax execution
- Debug step by step
- Verify environment variables

#### Common Syntax Errors to Watch For

**Error 1: Missing quotes**

```groovy
// Wrong
echo Hello World

// Correct
echo 'Hello World'
```

**Error 2: Wrong agent syntax**

```groovy
// Wrong
agent: any

// Correct
agent any
```

**Error 3: Stages must have stage**

```groovy
// Wrong
stages {
    echo 'test'
}

// Correct
stages {
    stage('Test') {
        steps {
            echo 'test'
        }
    }
}
```

**Error 4: Steps missing**

```groovy
// Wrong
stage('Build') {
    sh 'make'
}

// Correct
stage('Build') {
    steps {
        sh 'make'
    }
}
```



---

## Understanding Our Jenkinsfile

Let's break down the Jenkinsfile in this project section by section.

### Overall Structure

```groovy
pipeline {
    agent any           // Where to run
    options { }         // Pipeline options
    parameters { }      // Build parameters
    environment { }     // Environment variables
    stages { }          // Build stages
    post { }           // Post-build actions
}
```

---

## Step-by-Step Breakdown

### 1. Agent Declaration

```groovy
agent any
```

**What it does:**

- Tells Jenkins where to execute the pipeline
- `any` means "run on any available agent"

**Other options:**

```groovy
agent {
    label 'linux'           // Specific agent
}

agent {
    docker {                // Run in Docker
        image 'python:3.9'
    }
}

agent none                  // Define per-stage
```

### 2. Options Section

```groovy
options {
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timeout(time: 30, unit: 'MINUTES')
    timestamps()
}
```

**buildDiscarder:**

- Keeps only last 10 builds
- Prevents disk space issues
- Automatic cleanup

**timeout:**

- Pipeline fails after 30 minutes
- Prevents hung builds
- Saves resources

**timestamps:**

- Adds timestamp to console output
- Easier debugging
- Track slow steps

### 3. Parameters Section

```groovy
parameters {
    string(name: 'BRANCH', defaultValue: 'main', 
           description: 'Git branch to checkout')
    choice(name: 'ENVIRONMENT', 
           choices: ['dev', 'staging', 'prod'], 
           description: 'Deployment environment')
}
```

**Why use parameters?**

- Make pipeline flexible
- User can select options
- Same pipeline, different configurations

**Accessing parameters:**

```groovy
echo "Building branch: ${params.BRANCH}"
echo "Deploying to: ${params.ENVIRONMENT}"
```

**Parameter types:**

```groovy
string(name: 'VERSION', defaultValue: '1.0.0')
booleanParam(name: 'SKIP_TESTS', defaultValue: false)
choice(name: 'ENV', choices: ['dev', 'prod'])
password(name: 'SECRET', defaultValue: '')
```

### 4. Environment Variables

```groovy
environment {
    PYTHONPATH = "${WORKSPACE}/src"
}
```

**WORKSPACE:**

- Jenkins built-in variable
- Points to job's workspace directory
- Example: `/var/jenkins_home/workspace/my-job`

**Setting environment variables:**

```groovy
environment {
    // Static
    APP_NAME = 'my-app'
    
    // Dynamic (from Jenkins)
    BUILD_VERSION = "${BUILD_NUMBER}"
    
    // From parameters
    DEPLOY_ENV = "${params.ENVIRONMENT}"
}
```

**Using environment variables:**

```groovy
steps {
    sh 'echo $APP_NAME'
    echo "App: ${env.APP_NAME}"
}
```

### 5. Stages Section

This is where the actual work happens. Each stage represents a phase in your CI/CD process.

#### Stage 1: Checkout

```groovy
stage('Checkout') {
    steps {
        echo "Checking out code from ${params.BRANCH} branch..."
        checkout scm
        
        script {
            env.GIT_COMMIT_MSG = sh(
                script: 'git log -1 --pretty=%B',
                returnStdout: true
            ).trim()
            env.GIT_AUTHOR = sh(
                script: 'git log -1 --pretty=%an',
                returnStdout: true
            ).trim()
            env.GIT_COMMIT_HASH = sh(
                script: 'git log -1 --pretty=%h',
                returnStdout: true
            ).trim()
        }
        
        echo "Latest commit: ${env.GIT_COMMIT_MSG}"
        echo "Author: ${env.GIT_AUTHOR}"
        echo "Commit hash: ${env.GIT_COMMIT_HASH}"
    }
}
```

**What happens:**

1. **checkout scm**: Clones the Git repository
2. **script block**: Runs Groovy code for complex logic
3. **sh()**: Executes shell commands
4. **returnStdout: true**: Captures command output
5. **.trim()**: Removes whitespace

**Why capture Git info?**

- Traceability: Know what was built
- Artifacts: Tag builds with commit info
- Notifications: Send commit details to team

#### Stage 2: Create Virtual Environment

```groovy
stage('Create Virtual Environment') {
    steps {
        echo "Creating Python virtual environment..."
        sh '''
            # Remove existing venv if it exists to ensure clean state
            rm -rf .venv
            
            # Check if python3 is available, fallback to python
            if command -v python3 >/dev/null 2>&1; then
                PYTHON_CMD=python3
            elif command -v python >/dev/null 2>&1; then
                PYTHON_CMD=python
            else
                echo "ERROR: No Python interpreter found!"
                exit 1
            fi
            
            echo "Using Python: $PYTHON_CMD"
            $PYTHON_CMD --version
            
            # Create virtual environment
            echo "Creating new virtual environment..."
            $PYTHON_CMD -m venv .venv --without-pip
            
            # Manually install pip if needed
            if [ ! -f .venv/bin/pip ]; then
                echo "Installing pip manually..."
                curl -s https://bootstrap.pypa.io/get-pip.py | .venv/bin/python
            fi
            
            # Activate and upgrade pip
            . .venv/bin/activate
            python -m pip install --upgrade pip setuptools wheel
            echo "Virtual environment ready"
        '''
    }
}
```

**Shell Script Block (`sh '''...'''`):**

- Multi-line shell script
- Runs in bash/sh
- Triple quotes for multi-line

**Key techniques:**

1. **Clean state**: Remove old venv
2. **Fallback logic**: Try python3, then python
3. **Error handling**: Exit if no Python found
4. **Conditional execution**: Install pip if missing
5. **Tool upgrade**: Update pip/setuptools

**Why virtual environment?**

- Isolated dependencies
- Reproducible builds
- No system pollution
- Clean for each build

#### Stage 3: Install Dependencies

```groovy
stage('Install Dependencies') {
    steps {
        echo "Installing dependencies from requirements.txt..."
        sh '''
            . .venv/bin/activate
            pip install -r requirements.txt
            echo "Dependencies installed"
            pip list
        '''
    }
}
```

**What happens:**

1. Activate virtual environment
2. Install from requirements.txt
3. List installed packages (for logs)

**Why list packages?**

- Verify installation
- Debug dependency issues
- Document build environment

#### Stage 4: Code Quality - Linting

```groovy
stage('Code Quality - Linting') {
    steps {
        echo "Running pylint for code quality analysis..."
        sh '''
            . .venv/bin/activate
            pylint src/ || true
            echo "Linting completed"
        '''
    }
}
```

**|| true pattern:**

- Command may fail (linting errors)
- `|| true` prevents pipeline failure
- Pipeline continues even with warnings

**When to use `|| true`:**

- Quality checks (warnings ok)
- Optional steps
- Informational commands

**When NOT to use:**

- Critical steps
- Security checks (must pass)
- Build compilation

#### Stage 5: Code Formatting Check

```groovy
stage('Code Formatting Check') {
    steps {
        echo "Checking code formatting with black..."
        sh '''
            . .venv/bin/activate
            black --check --diff src/ tests/ || true
            echo "Code formatting check completed"
        '''
    }
}
```

**Black formatter flags:**

- `--check`: Don't modify files, just check
- `--diff`: Show what would change
- Helps maintain consistent code style

#### Stage 6: Unit Tests

```groovy
stage('Unit Tests') {
    steps {
        echo "Running unit tests with coverage..."
        sh '''
            . .venv/bin/activate
            mkdir -p build/artifacts
            
            # Run tests with coverage
            pytest tests/ --junitxml=build/artifacts/test-results.xml \
                           --cov=src \
                           --cov-report=html:build/artifacts/htmlcov \
                           --cov-report=xml:build/artifacts/coverage.xml \
                           --cov-report=term
            
            echo "Tests completed"
        '''
    }
}
```

**pytest flags explained:**

- `--junitxml`: JUnit format for Jenkins
- `--cov=src`: Measure coverage of src/
- `--cov-report=html`: HTML coverage report
- `--cov-report=xml`: XML for tools
- `--cov-report=term`: Terminal output

**Why multiple report formats?**

- JUnit: Jenkins integration
- HTML: Human-readable
- XML: Tool processing
- Term: Immediate feedback

#### Stage 7: Build Artifacts

```groovy
stage('Build Artifacts') {
    steps {
        echo "Building application artifacts..."
        sh '''
            . .venv/bin/activate
            mkdir -p build/artifacts
            
            # Create distribution package
            python setup.py sdist bdist_wheel
            
            # Copy artifacts
            cp dist/*.tar.gz build/artifacts/ || true
            cp dist/*.whl build/artifacts/ || true
            
            # Create version file
            echo "Build: ${BUILD_NUMBER}" > build/artifacts/build-info.txt
            echo "Commit: ${GIT_COMMIT_HASH}" >> build/artifacts/build-info.txt
            echo "Branch: main" >> build/artifacts/build-info.txt
            echo "Author: ${GIT_AUTHOR}" >> build/artifacts/build-info.txt
            echo "Date: $(date)" >> build/artifacts/build-info.txt
            
            echo "Artifacts built successfully"
        '''
    }
}
```

**Python packaging:**

- `sdist`: Source distribution (.tar.gz)
- `bdist_wheel`: Binary distribution (.whl)
- Both formats for compatibility

**Build metadata file:**

- Documents what was built
- Traceability
- Debugging production issues

#### Stage 8: Security Scan

```groovy
stage('Security Scan') {
    steps {
        echo "Running security checks with bandit..."
        sh '''
            . .venv/bin/activate
            mkdir -p build/artifacts
            
            # Install bandit if not available
            pip install bandit || true
            
            bandit -r src/ -f json -o build/artifacts/bandit-report.json || true
            bandit -r src/ -f txt || true
            
            echo "Security scan completed"
        '''
    }
}
```

**Bandit security scanner:**

- Finds common security issues
- SQL injection risks
- Hardcoded passwords
- Insecure functions

**Report formats:**

- JSON: Machine-readable
- TXT: Human-readable console output

#### Stage 9: Deploy (Conditional)

```groovy
stage('Deploy') {
    when {
        branch 'main'
    }
    steps {
        echo "Deploying to ${params.ENVIRONMENT}..."
        sh '''
            . .venv/bin/activate
            chmod +x ./scripts/deploy-${ENVIRONMENT}.sh
            ./scripts/deploy-${ENVIRONMENT}.sh
        '''
    }
}
```

**when directive:**

- Conditional stage execution
- Only runs on main branch
- Prevents accidental deploys from feature branches

**Other when conditions:**

```groovy
when {
    branch 'main'                    // Specific branch
    expression { params.DEPLOY }     // Parameter check
    environment name: 'ENV', value: 'prod'  // Env var
    allOf {                          // Multiple conditions
        branch 'main'
        environment name: 'ENV', value: 'prod'
    }
}
```

#### Stage 10: Health Check

```groovy
stage('Health Check') {
    steps {
        echo "Running application health check..."
        sh '''
            . .venv/bin/activate
            export PYTHONPATH="${WORKSPACE}/src:${PYTHONPATH}"
            python src/app.py
            echo "Application health check passed"
        '''
    }
}
```

**Why health check?**

- Verify app can start
- Catch import errors
- Basic smoke test

#### Stage 11: Cleanup (Conditional)

```groovy
stage('Cleanup Virtual Environment') {
    when {
        expression { params.ENVIRONMENT == 'prod' }
    }
    steps {
        echo "Cleaning up virtual environment cache..."
        sh '''
            . .venv/bin/activate
            pip cache purge || true
            echo "Cache cleaned"
        '''
    }
}
```

**Conditional cleanup:**

- Only for production deploys
- Saves disk space
- Removes cached packages

### 6. Post Section

```groovy
post {
    always {
        echo "Collecting build artifacts..."
        
        // Publish test results
        junit testResults: 'build/artifacts/test-results.xml', 
              allowEmptyResults: true
        
        // Archive all artifacts
        archiveArtifacts artifacts: 'build/artifacts/**', 
                        allowEmptyArchive: true
        
        // Show environment info
        sh '''
            if [ -f .venv/bin/activate ]; then
                . .venv/bin/activate
                echo "Python Environment Info:"
                python --version
                pip --version
                echo "Installed packages:"
                pip list
            else
                echo "Virtual environment not available for cleanup"
            fi
        '''
    }
    
    success {
        echo "Pipeline completed successfully!"
        echo "Build URL: ${BUILD_URL}"
        echo "Coverage Report: Check archived artifacts -> build/artifacts/htmlcov/index.html"
        echo "Test Results: ${BUILD_URL}testReport/"
        echo "Artifacts: ${BUILD_URL}artifact/"
    }
    
    failure {
        echo "Pipeline failed!"
        echo "Build URL: ${BUILD_URL}"
        echo "Console Logs: ${BUILD_URL}console"
    }
    
    unstable {
        echo "WARNING: Pipeline is unstable (tests failed)"
    }
}
```

**Post conditions:**

- **always**: Runs no matter what
- **success**: Only on successful build
- **failure**: Only on failed build
- **unstable**: Tests failed but build passed
- **changed**: Build status changed

**Jenkins built-in steps:**

- `junit`: Publish test results
- `archiveArtifacts`: Save build outputs
- Both integrate with Jenkins UI

---

## Best Practices

### 1. Use Declarative Pipeline

```groovy
// Good
pipeline {
    agent any
    stages { }
}

// Avoid (unless you need the flexibility)
node {
    stage('Build') { }
}
```

### 2. Fail Fast

```groovy
// Good - Stop on critical failures
sh 'pytest tests/'

// Bad - Continue on critical failures
sh 'pytest tests/ || true'
```

### 3. Keep Stages Small

```groovy
// Good - Single responsibility
stage('Test') { }
stage('Build') { }
stage('Deploy') { }

// Bad - Too much in one stage
stage('Test Build Deploy') { }
```

### 4. Use Meaningful Names

```groovy
// Good
stage('Run Unit Tests with Coverage') { }

// Bad
stage('Step 3') { }
```

### 5. Clean Up Resources

```groovy
post {
    always {
        cleanWs()  // Clean workspace
        sh 'docker system prune -f'  // Clean Docker
    }
}
```

### 6. Use Environment Variables

```groovy
// Good
environment {
    APP_VERSION = "1.0.${BUILD_NUMBER}"
}
steps {
    sh 'echo Building version $APP_VERSION'
}

// Bad - Hardcoded values
steps {
    sh 'echo Building version 1.0.5'
}
```

### 7. Parallelize When Possible

```groovy
stage('Tests') {
    parallel {
        stage('Unit Tests') {
            steps {
                sh 'pytest tests/unit/'
            }
        }
        stage('Integration Tests') {
            steps {
                sh 'pytest tests/integration/'
            }
        }
    }
}
```

### 8. Add Timeouts

```groovy
// Stage-level timeout
stage('Deploy') {
    options {
        timeout(time: 10, unit: 'MINUTES')
    }
    steps {
        sh './deploy.sh'
    }
}
```

### 9. Use Credentials Securely

```groovy
environment {
    // Never do this
    PASSWORD = 'mysecretpass'
}

// Instead use Jenkins credentials
environment {
    MY_SECRET = credentials('my-secret-id')
}
```

### 10. Version Your Jenkinsfile

```bash
# Track changes
git log Jenkinsfile

# Review changes before merging
git diff main feature/new-pipeline Jenkinsfile
```

---

## Common Patterns

### Pattern 1: Matrix Builds

Test on multiple Python versions:

```groovy
pipeline {
    agent none
    stages {
        stage('Test') {
            matrix {
                axes {
                    axis {
                        name 'PYTHON_VERSION'
                        values '3.8', '3.9', '3.10', '3.11'
                    }
                }
                agent {
                    docker {
                        image "python:${PYTHON_VERSION}"
                    }
                }
                stages {
                    stage('Test') {
                        steps {
                            sh 'python --version'
                            sh 'pip install -r requirements.txt'
                            sh 'pytest'
                        }
                    }
                }
            }
        }
    }
}
```

### Pattern 2: Input Step

Manual approval before deploy:

```groovy
stage('Deploy to Production') {
    steps {
        input message: 'Deploy to production?', 
              ok: 'Deploy'
        sh './deploy-prod.sh'
    }
}
```

### Pattern 3: Retry Logic

Retry flaky tests:

```groovy
stage('Integration Tests') {
    steps {
        retry(3) {
            sh 'pytest tests/integration/'
        }
    }
}
```

### Pattern 4: Stash/Unstash

Share files between agents:

```groovy
stage('Build') {
    steps {
        sh 'make build'
        stash name: 'build-artifacts', includes: 'dist/**'
    }
}
stage('Deploy') {
    agent { label 'deployment-server' }
    steps {
        unstash 'build-artifacts'
        sh './deploy.sh'
    }
}
```

### Pattern 5: Custom Workspace

Use specific directory:

```groovy
pipeline {
    agent {
        node {
            label 'linux'
            customWorkspace '/var/builds/my-project'
        }
    }
}
```

---

## Troubleshooting

### Problem 1: Pipeline Fails at Checkout

**Error:**

```text
ERROR: Error cloning remote repo 'origin'
```

**Solution:**

```groovy
// Make sure credentials are configured
checkout([
    $class: 'GitSCM',
    branches: [[name: '*/main']],
    userRemoteConfigs: [[
        url: 'https://github.com/user/repo.git',
        credentialsId: 'github-credentials'
    ]]
])
```

### Problem 2: Environment Variables Not Working

**Error:**

```text
Variable not set: PYTHON_CMD
```

**Solution:**

```groovy
// Use env. prefix
echo "${env.WORKSPACE}"

// Or in shell
sh 'echo $WORKSPACE'

// Not in Groovy strings
echo "$WORKSPACE"  // This won't work
```

### Problem 3: Multi-line Strings

**Error:**

```text
Unexpected character: '
```

**Solution:**

```groovy
// Use triple quotes for multi-line
sh '''
    line 1
    line 2
    line 3
'''

// Or escape newlines
sh "line 1 \
    line 2 \
    line 3"
```

### Problem 4: Parallel Stage Failures

**Error:**

```text
One or more parallel branches failed
```

**Solution:**

```groovy
parallel {
    stage('Test 1') {
        steps {
            catchError(buildResult: 'UNSTABLE') {
                sh 'pytest tests/unit'
            }
        }
    }
}
```

### Problem 5: Workspace Cleanup

**Error:**

```text
Disk full
```

**Solution:**

```groovy
post {
    always {
        cleanWs()
        sh 'docker system prune -f'
    }
}
```

---

## Quick Reference

### Common Jenkins Variables

```groovy
BUILD_NUMBER        // Build number (e.g., 42)
BUILD_ID            // Build ID (same as BUILD_NUMBER)
BUILD_URL           // Full URL to build
JOB_NAME            // Name of the job
WORKSPACE           // Workspace directory path
GIT_COMMIT          // Git commit SHA
GIT_BRANCH          // Git branch name
NODE_NAME           // Agent name
```

### Common Pipeline Steps

```groovy
// Shell commands
sh 'command'
sh(script: 'command', returnStdout: true)

// Echo messages
echo 'message'

// Error handling
error('Build failed')
catchError(buildResult: 'UNSTABLE') { }

// Conditionals
when { }

// File operations
archiveArtifacts 'build/**'
stash name: 'source'
unstash 'source'

// Time
timeout(time: 1, unit: 'HOURS') { }
sleep time: 30, unit: 'SECONDS'

// Retry
retry(3) { }

// Parallel
parallel { }
```

### Post Conditions

```groovy
post {
    always { }      // Always runs
    success { }     // Only on success
    failure { }     // Only on failure
    unstable { }    // Tests failed
    changed { }     // Status changed
    aborted { }     // Build aborted
    cleanup { }     // After other post blocks
}
```

---

## Next Steps

1. **Modify the Jenkinsfile**: Try adding a new stage
2. **Add notifications**: Email or Slack on build failure
3. **Implement Docker**: Run builds in containers
4. **Add shared libraries**: Reuse code across pipelines
5. **Set up webhooks**: Automatic builds on Git push

---

## Additional Resources

- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Pipeline Syntax Reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Pipeline Steps Reference](https://www.jenkins.io/doc/pipeline/steps/)
- [Best Practices](https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/)

---

**Happy Building!**