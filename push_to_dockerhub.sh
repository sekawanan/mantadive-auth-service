#!/bin/bash

# =====================================================================
# Script Name: push_to_dockerhub.sh
# Description: Builds the Docker image for FastAPI Auth Service, tags it,
#              and pushes it to DockerHub.
# Usage: ./push_to_dockerhub.sh [IMAGE_NAME] [TAG]
#        Defaults:
#          IMAGE_NAME: fastapi-auth-service
#          TAG: latest
# =====================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# ---------------------
# Configuration
# ---------------------

# Default values
DEFAULT_IMAGE_NAME="mantadive-auth-service"
DEFAULT_TAG="latest"

# Usage function
usage() {
  echo "Usage: $0 [IMAGE_NAME] [TAG]"
  echo "Defaults:"
  echo "  IMAGE_NAME: $DEFAULT_IMAGE_NAME"
  echo "  TAG: $DEFAULT_TAG"
  exit 1
}

# ---------------------
# Input Arguments
# ---------------------

IMAGE_NAME=${1:-$DEFAULT_IMAGE_NAME}
TAG=${2:-$DEFAULT_TAG}

# ---------------------
# DockerHub Configuration
# ---------------------

# Ensure DOCKERHUB_USERNAME is set
if [ -z "$DOCKERHUB_USERNAME" ]; then
  echo "Error: DOCKERHUB_USERNAME environment variable is not set."
  echo "Please set it using 'export DOCKERHUB_USERNAME=your_username' and try again."
  exit 1
fi

# Optionally, you can set DOCKERHUB_PASSWORD as an environment variable
# for non-interactive login, but it's recommended to handle authentication
# securely. Avoid hardcoding passwords in scripts.
# Uncomment the following lines if you wish to enable this feature.
#
if [ -z "$DOCKERHUB_PASSWORD" ]; then
  echo "Error: DOCKERHUB_PASSWORD environment variable is not set."
  echo "Please set it using 'export DOCKERHUB_PASSWORD=your_password' and try again."
  exit 1
fi

echo "Logging in to DockerHub..."
echo $DOCKERHUB_PASSWORD | docker login -u $DOCKERHUB_USERNAME --password-stdin


# ---------------------
# Build the Docker Image
# ---------------------

echo "=============================="
echo " Building the Docker image..."
echo "=============================="

docker build -t ${IMAGE_NAME}:${TAG} .

# ---------------------
# Tag the Docker Image
# ---------------------

FULL_IMAGE_NAME="${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}"

echo "=============================="
echo " Tagging the Docker image..."
echo "=============================="

docker tag ${IMAGE_NAME}:${TAG} ${FULL_IMAGE_NAME}

# ---------------------
# Push the Docker Image
# ---------------------

echo "=============================="
echo " Pushing the Docker image to DockerHub..."
echo "=============================="

docker push ${FULL_IMAGE_NAME}

echo "========================================="
echo " Docker image pushed successfully to ${FULL_IMAGE_NAME}"
echo "========================================="
