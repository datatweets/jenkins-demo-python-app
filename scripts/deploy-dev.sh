#!/bin/bash
set -e

echo "Deploying to DEV environment..."
echo "Deployment started at: $(date)"
echo "Build Number: ${BUILD_NUMBER:-unknown}"
echo "Git Commit: ${GIT_COMMIT_HASH:-unknown}"

echo ""
echo "Available build artifacts:"
if [ -d "build/artifacts" ]; then
    ls -lh build/artifacts/
    echo ""
    echo "Build information:"
    if [ -f "build/artifacts/build-info.txt" ]; then
        cat build/artifacts/build-info.txt
    else
        echo "WARNING: build-info.txt not found"
    fi
else
    echo "WARNING: build/artifacts directory not found"
fi

echo ""
echo "Simulating deployment steps:"
echo "  1. Validating artifacts..."
sleep 1
echo "  2. Deploying to DEV server..."
sleep 2
echo "  3. Running health checks..."
sleep 1
echo "  4. Updating load balancer..."
sleep 1

echo ""
echo "Deployment to DEV environment completed successfully!"
echo "Application should be available at: http://dev-server.example.com"
echo "Deployment finished at: $(date)"
