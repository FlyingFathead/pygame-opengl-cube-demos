#!/bin/bash

# Define variables
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
MAIN_SCRIPT="cube_libre.py"

# Function to display messages
echo_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

echo_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo_error "Python3 could not be found. Please install Python3."
    exit 1
fi

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null
then
    echo_info "pip3 not found. Installing pip3..."
    sudo apt update
    sudo apt install -y python3-pip
    if ! command -v pip3 &> /dev/null
    then
        echo_error "pip3 installation failed. Please install pip3 manually."
        exit 1
    fi
fi

# Check if virtualenv is installed
if ! python3 -m pip show virtualenv &> /dev/null
then
    echo_info "virtualenv not found. Installing virtualenv..."
    python3 -m pip install --user virtualenv
    if ! python3 -m pip show virtualenv &> /dev/null
    then
        echo_error "virtualenv installation failed. Please install virtualenv manually."
        exit 1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo_info "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo_error "Failed to create virtual environment."
        exit 1
    fi
else
    echo_info "Virtual environment already exists."
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
    echo_error "Failed to activate virtual environment."
    exit 1
fi

# Upgrade pip
echo_info "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo_info "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
    if [ $? -ne 0 ]; then
        echo_error "Failed to install dependencies."
        deactivate
        exit 1
    fi
else
    echo_error "$REQUIREMENTS_FILE not found."
    deactivate
    exit 1
fi

# Run the main script
if [ -f "$MAIN_SCRIPT" ]; then
    echo_info "Running $MAIN_SCRIPT..."
    python "$MAIN_SCRIPT"
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo_error "$MAIN_SCRIPT exited with code $EXIT_CODE."
    fi
else
    echo_error "$MAIN_SCRIPT not found."
    deactivate
    exit 1
fi

# Deactivate the virtual environment
deactivate
