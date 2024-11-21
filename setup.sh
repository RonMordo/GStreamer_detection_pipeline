#!/bin/bash

# Check for superuser privileges for system-level installation
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo) to install system-level dependencies."
  exit 1
fi

echo "Starting setup..."

# Step 1: Install system-level dependencies
echo "Installing system-level dependencies..."
apt update -y
apt install -y python3 python3-venv python3-pip \
    gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav \
    libsm6 libxext6 libxrender-dev ffmpeg \
    python3-gi python3-gi-cairo gir1.2-gstreamer-1.0 \
    libcairo2-dev libxt-dev libgirepository1.0-dev

# Step 2: Install Python packages (PyGObject and pycairo via pip)
echo "Installing PyGObject and pycairo via pip..."
pip3 install --upgrade pip

# Step 3: Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 4: Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo "Activate the environment using 'source venv/bin/activate'."

