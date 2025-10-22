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
        ARTIFACT_DIR = "${WORKSPACE}/build/artifacts"
        JENKINS_URL = 'https://delores-lordlier-vania.ngrok-free.dev'
        VENV_DIR = "${WORKSPACE}/.venv"
        VENV_BIN = "${WORKSPACE}/.venv/bin"
        PYTHONPATH = "${WORKSPACE}/src:${PYTHONPATH}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo "🔄 Checking out code from ${params.BRANCH} branch..."
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
                
                echo "✅ Latest commit: ${env.GIT_COMMIT_MSG}"
                echo "📝 Author: ${env.GIT_AUTHOR}"
                echo "🔗 Commit hash: ${env.GIT_COMMIT_HASH}"
            }
        }
        
        stage('Create Virtual Environment') {
            steps {
                echo "🔧 Creating Python virtual environment..."
                sh '''
                    # Check if .venv exists, if not create it
                    if [ ! -d "${VENV_DIR}" ]; then
                        echo "Creating new virtual environment..."
                        python3 -m venv ${VENV_DIR}
                    else
                        echo "Virtual environment already exists, reusing it..."
                    fi
                    
                    # Activate and upgrade pip
                    . ${VENV_BIN}/activate
                    python3 -m pip install --upgrade pip setuptools wheel
                    echo "✅ Virtual environment ready"
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo "📦 Installing dependencies from requirements.txt..."
                sh '''
                    . ${VENV_BIN}/activate
                    pip install -r requirements.txt
                    echo "✅ Dependencies installed"
                    pip list
                '''
            }
        }
        
        stage('Code Quality - Linting') {
            steps {
                echo "📊 Running pylint for code quality..."
                sh '''
                    mkdir -p ${ARTIFACT_DIR}
                    . ${VENV_BIN}/activate
                    
                    pylint src/app.py --exit-zero --output-format=parseable > ${ARTIFACT_DIR}/pylint-report.txt || true
                    cat ${ARTIFACT_DIR}/pylint-report.txt
                '''
            }
        }
        
        stage('Code Formatting Check') {
            steps {
                echo "✨ Checking code formatting with black..."
                sh '''
                    . ${VENV_BIN}/activate
                    black --check src/ tests/ || echo "Code formatting issues found (non-blocking)"
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo "🧪 Running unit tests with pytest..."
                sh '''
                    . ${VENV_BIN}/activate
                    mkdir -p ${ARTIFACT_DIR}
                    
                    pytest tests/ -v \
                        --junit-xml=${ARTIFACT_DIR}/test-results.xml \
                        --cov=src \
                        --cov-report=xml:${ARTIFACT_DIR}/coverage.xml \
                        --cov-report=html:${ARTIFACT_DIR}/htmlcov \
                        --cov-report=term-missing
                    
                    echo "✅ Tests completed"
                '''
            }
        }
        
        stage('Build Artifacts') {
            steps {
                echo "📦 Creating distribution artifacts..."
                sh '''
                    . ${VENV_BIN}/activate
                    mkdir -p ${ARTIFACT_DIR}
                    
                    # Create source distribution
                    python3 setup.py sdist --dist-dir=${ARTIFACT_DIR}
                    
                    # Create wheel distribution
                    python3 -m pip install wheel --quiet
                    python3 setup.py bdist_wheel --dist-dir=${ARTIFACT_DIR}
                    
                    # Create a tarball of the entire source
                    tar -czf ${ARTIFACT_DIR}/source.tar.gz \
                        --exclude=.venv \
                        --exclude=__pycache__ \
                        --exclude=.pytest_cache \
                        --exclude=.coverage \
                        --exclude=htmlcov \
                        --exclude=.git \
                        .
                    
                    # List all artifacts
                    echo "📋 Artifacts created:"
                    ls -lh ${ARTIFACT_DIR}/
                '''
            }
        }
        
        stage('Security Scan') {
            steps {
                echo "🔒 Running security checks with bandit..."
                sh '''
                    . ${VENV_BIN}/activate
                    mkdir -p ${ARTIFACT_DIR}
                    
                    bandit -r src/ -f json -o ${ARTIFACT_DIR}/bandit-report.json || true
                    bandit -r src/ -f txt || true
                    
                    echo "✅ Security scan completed"
                '''
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo "🚀 Deploying to ${params.ENVIRONMENT}..."
                sh '''
                    . ${VENV_BIN}/activate
                    chmod +x ./scripts/deploy-${ENVIRONMENT}.sh
                    ./scripts/deploy-${ENVIRONMENT}.sh
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                echo "💚 Running application health check..."
                sh '''
                    . ${VENV_BIN}/activate
                    export PYTHONPATH="${WORKSPACE}/src:${PYTHONPATH}"
                    python3 src/app.py
                    echo "✅ Application health check passed"
                '''
            }
        }
        
        stage('Cleanup Virtual Environment') {
            when {
                expression { params.ENVIRONMENT == 'prod' }
            }
            steps {
                echo "🧹 Cleaning up virtual environment cache..."
                sh '''
                    . ${VENV_BIN}/activate
                    pip cache purge || true
                    echo "✅ Cache cleaned"
                '''
            }
        }
    }
    
    post {
        always {
            echo "📋 Collecting build artifacts..."
            
            // Publish test results
            junit testResults: '${ARTIFACT_DIR}/test-results.xml', 
                  allowEmptyResults: true
            
            // Publish code coverage
            publishHTML([
                reportDir: '${ARTIFACT_DIR}/htmlcov',
                reportFiles: 'index.html',
                reportName: 'Code Coverage Report',
                allowMissing: true
            ])
            
            // Archive all artifacts
            archiveArtifacts artifacts: 'build/artifacts/**', 
                            allowEmptyArchive: true
            
            // Show environment info
            sh '''
                . ${VENV_BIN}/activate
                echo "📊 Python Environment Info:"
                python3 --version
                pip --version
                echo "Installed packages:"
                pip list
            '''
        }
        
        success {
            echo "✅ Pipeline completed successfully!"
            echo "📍 View at: ${JENKINS_URL}/job/jenkins-demo-python-app/${BUILD_NUMBER}/"
            echo "📊 Coverage Report: ${JENKINS_URL}/job/jenkins-demo-python-app/${BUILD_NUMBER}/Code_Coverage_Report/"
        }
        
        failure {
            echo "❌ Pipeline failed!"
            echo "📍 View logs at: ${JENKINS_URL}/job/jenkins-demo-python-app/${BUILD_NUMBER}/console"
        }
        
        unstable {
            echo "⚠️ Pipeline is unstable (tests failed)"
        }
    }
}
