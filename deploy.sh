#!/bin/bash

# Exit on error
set -e

# Get the project ID from gcloud config
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "Error: No project ID set. Please run 'gcloud config set project [PROJECT-ID]' first."
    exit 1
fi

echo "Deploying to project: $PROJECT_ID"

# Build the Docker image
echo "Building Docker image..."
docker build -t gcr.io/$PROJECT_ID/mc-verify-api .

# Push the image to Google Container Registry
echo "Pushing image to Google Container Registry..."
docker push gcr.io/$PROJECT_ID/mc-verify-api

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy mc-verify-api \
  --image gcr.io/$PROJECT_ID/mc-verify-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Get the service URL
SERVICE_URL=$(gcloud run services describe mc-verify-api --platform managed --region us-central1 --format 'value(status.url)')
echo "Deployment complete! Service URL: $SERVICE_URL"

# Run tests
echo "Running tests..."
./test_cloud_run.sh