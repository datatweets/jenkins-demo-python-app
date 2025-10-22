pipeline {
    agent any
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }
    
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to checkout')
        choice(name: 'ENVIRONMENT', choices: ['dev', 'staging', 'prod'], description: 'Deployment environment')
    }
    
    environment {
        PYTHONPATH = "${WORKSPACE}/src"
    }
    
    stages {
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
    }
    
    post {
        always {
            echo "Collecting build artifacts..."
            
            // Publish test results
            junit testResults: 'build/artifacts/test-results.xml', 
                  allowEmptyResults: true
            
            // Archive all artifacts (including coverage reports)
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
}
