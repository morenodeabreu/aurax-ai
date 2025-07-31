#!/bin/bash
set -e

echo "Installing Playwright browser dependencies..."

# Install system dependencies required by Playwright
apt-get update && apt-get install -y \
    libnss3-dev \
    libatk-bridge2.0-dev \
    libdrm-dev \
    libxkbcommon-dev \
    libgtk-3-dev \
    libgbm-dev \
    libasound2-dev

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium

# Install browser dependencies
echo "Installing Playwright system dependencies..."
playwright install-deps chromium

echo "Playwright installation completed successfully!"