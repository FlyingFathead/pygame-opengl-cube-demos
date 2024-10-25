#!/bin/bash

# =====================
# Configuration Section
# =====================

# Function to detect the operating system and set PYTHON_EXEC
detect_python_exec() {
    # Use uname to get the operating system name
    OS_NAME="$(uname -s)"
    
    case "${OS_NAME}" in
        Linux*)
            echo "python3"
            ;;
        Darwin*)
            echo "python3"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "python"
            ;;
        *)
            # Default to python3 if OS is unrecognized
            echo "python3"
            ;;
    esac
}

# You can i.e. manually set the executable to 'python3' or 'python' based on your environment.
# For Windows with Git Bash, you might need to change it to 'python' instead of 'python3'.
# Set PYTHON_EXEC based on the detected OS
# PYTHON_EXEC="python3"
PYTHON_EXEC=$(detect_python_exec)

# Define other variables
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
MAIN_SCRIPT="cube_libre.py"

# ================
# Helper Functions
# ================

# Function to display informational messages
echo_info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

# Function to display error messages
echo_error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Function to compare Python versions
# Returns 0 (true) if $1 >= $2
version_ge() {
    # sort -V sorts versions correctly, we check if $1 is first or equal to $2
    [ "$(printf '%s\n' "$2" "$1" | sort -V | head -n1)" = "$2" ]
}

# =======================
# Setup Python Executable
# =======================

# Check if the defined Python executable exists
echo_info "Detected Python executable: $PYTHON_EXEC"

# Check if the defined Python executable exists
if ! command_exists "$PYTHON_EXEC"; then
    echo_error "$PYTHON_EXEC could not be found. Please install Python (version >= 3.10)."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$($PYTHON_EXEC -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')
REQUIRED_VERSION="3.10"

# Compare versions
if version_ge "$PYTHON_VERSION" "$REQUIRED_VERSION"; then
    echo_info "Python version $PYTHON_VERSION meets the requirement."
else
    echo_error "Python version $PYTHON_VERSION is lower than the required version $REQUIRED_VERSION."
    exit 1
fi

# =========
# Setup pip
# =========

# Define pip executable using the Python executable
PIP_EXEC="$PYTHON_EXEC -m pip"

# Check if pip is installed
if ! $PIP_EXEC --version &> /dev/null; then
    echo_info "pip not found. Attempting to install pip..."
    
    # Attempt to install pip using ensurepip
    $PYTHON_EXEC -m ensurepip --upgrade
    if ! $PIP_EXEC --version &> /dev/null; then
        echo_error "pip installation failed. Please install pip manually."
        exit 1
    fi
fi

echo_info "pip is installed."

# ================
# Setup virtualenv
# ================

# Check if virtualenv is installed
if ! $PIP_EXEC show virtualenv &> /dev/null; then
    echo_info "virtualenv not found. Installing virtualenv..."
    $PIP_EXEC install --user virtualenv
    if ! $PIP_EXEC show virtualenv &> /dev/null; then
        echo_error "virtualenv installation failed. Please install virtualenv manually."
        exit 1
    fi
    echo_info "virtualenv installed successfully."
fi

# ==========================
# Create Virtual Environment
# ==========================

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo_info "Creating virtual environment..."
    $PYTHON_EXEC -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo_error "Failed to create virtual environment."
        exit 1
    fi
    echo_info "Virtual environment created."
else
    # Check if activate script exists
    if [ ! -f "$VENV_DIR/bin/activate" ] && [ ! -f "$VENV_DIR/Scripts/activate" ]; then
        echo_info "'$VENV_DIR' activate script not found. Recreating virtual environment..."
        rm -rf "$VENV_DIR"
        $PYTHON_EXEC -m venv "$VENV_DIR"
        if [ $? -ne 0 ]; then
            echo_error "Failed to recreate virtual environment."
            exit 1
        fi
        echo_info "Virtual environment recreated."
    else
        echo_info "Virtual environment already exists."
    fi
fi

# ============================
# Activate Virtual Environment
# ============================

# Determine the activation script based on the OS
if [ -f "$VENV_DIR/bin/activate" ]; then
    ACTIVATE_SCRIPT="$VENV_DIR/bin/activate"
elif [ -f "$VENV_DIR/Scripts/activate" ]; then
    ACTIVATE_SCRIPT="$VENV_DIR/Scripts/activate"
else
    echo_error "Activate script not found in virtual environment."
    exit 1
fi

# Activate the virtual environment
source "$ACTIVATE_SCRIPT"
if [ $? -ne 0 ]; then
    echo_error "Failed to activate virtual environment."
    exit 1
fi

echo_info "Virtual environment activated."

# ==========================================
# Upgrade pip within the Virtual Environment
# ==========================================

echo_info "Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo_error "Failed to upgrade pip."
    deactivate
    exit 1
fi
echo_info "pip upgraded successfully."

# ====================
# Install Dependencies
# ====================

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo_info "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
    if [ $? -ne 0 ]; then
        echo_error "Failed to install dependencies."
        deactivate
        exit 1
    fi
    echo_info "Dependencies installed successfully."
else
    echo_error "$REQUIREMENTS_FILE not found."
    deactivate
    exit 1
fi

# ===================
# Run the Main Script
# ===================

if [ -f "$MAIN_SCRIPT" ]; then

    # Detect if running under Wayland (Linux-specific)
    if [ -n "$WAYLAND_DISPLAY" ]; then
        echo_info "Wayland detected. Setting SDL_VIDEO_X11_FORCE_EGL=1 to force X11 with EGL."
        export SDL_VIDEO_X11_FORCE_EGL=1
    else
        echo_info "Wayland not detected. Proceeding with default settings."
    fi

    echo_info "Running $MAIN_SCRIPT..."
    $PYTHON_EXEC "$MAIN_SCRIPT"
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo_error "$MAIN_SCRIPT exited with code $EXIT_CODE."
    else
        echo_info "$MAIN_SCRIPT executed successfully."
    fi
else
    echo_error "$MAIN_SCRIPT not found."
    deactivate
    exit 1
fi

# ==============================
# Deactivate Virtual Environment
# ==============================

deactivate
echo_info "Virtual environment deactivated."

# =============
# End of Script
# =============

# // (old)
# #!/bin/bash

# # Define variables
# VENV_DIR="venv"
# REQUIREMENTS_FILE="requirements.txt"
# MAIN_SCRIPT="cube_libre.py"

# # Function to display messages
# echo_info() {
#     echo -e "\033[1;34m[INFO]\033[0m $1"
# }

# echo_error() {
#     echo -e "\033[1;31m[ERROR]\033[0m $1"
# }

# # Function to check if a command exists
# command_exists() {
#     command -v "$1" &> /dev/null
# }

# # Function to compare Python versions
# # Returns 0 (true) if $1 >= $2
# version_ge() {
#     # sort -V sorts versions correctly, we check if $1 is first or equal to $2
#     [ "$(printf '%s\n' "$2" "$1" | sort -V | head -n1)" = "$2" ]
# }

# # Check if Python 3 is installed
# if ! command_exists python3; then
#     echo_error "Python3 could not be found. Please install Python3 (version >= 3.10)."
#     exit 1
# fi

# # Get Python version
# PYTHON_VERSION=$(python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')
# REQUIRED_VERSION="3.10"

# # Compare versions
# if version_ge "$PYTHON_VERSION" "$REQUIRED_VERSION"; then
#     echo_info "Python version $PYTHON_VERSION meets the requirement."
# else
#     echo_error "Python version $PYTHON_VERSION is lower than the required version $REQUIRED_VERSION."
#     exit 1
# fi

# # Check if pip3 is installed
# if ! command_exists pip3; then
#     echo_info "pip3 not found. Installing pip3..."
#     sudo apt update
#     sudo apt install -y python3-pip
#     if ! command_exists pip3; then
#         echo_error "pip3 installation failed. Please install pip3 manually."
#         exit 1
#     fi
# fi

# # Check if virtualenv is installed
# if ! python3 -m pip show virtualenv &> /dev/null; then
#     echo_info "virtualenv not found. Installing virtualenv..."
#     python3 -m pip install --user virtualenv
#     if ! python3 -m pip show virtualenv &> /dev/null; then
#         echo_error "virtualenv installation failed. Please install virtualenv manually."
#         exit 1
#     fi
# fi

# # Create virtual environment if it doesn't exist
# if [ ! -d "$VENV_DIR" ]; then
#     echo_info "Creating virtual environment..."
#     python3 -m venv "$VENV_DIR"
#     if [ $? -ne 0 ]; then
#         echo_error "Failed to create virtual environment."
#         exit 1
#     fi
# else
#     # Check if activate script exists
#     if [ ! -f "$VENV_DIR/bin/activate" ]; then
#         echo_info "'$VENV_DIR/bin/activate' not found. Recreating virtual environment..."
#         rm -rf "$VENV_DIR"
#         python3 -m venv "$VENV_DIR"
#         if [ $? -ne 0 ]; then
#             echo_error "Failed to recreate virtual environment."
#             exit 1
#         fi
#     else
#         echo_info "Virtual environment already exists."
#     fi
# fi

# # Activate the virtual environment
# source "$VENV_DIR/bin/activate"
# if [ $? -ne 0 ]; then
#     echo_error "Failed to activate virtual environment."
#     exit 1
# fi

# # Upgrade pip within the virtual environment
# echo_info "Upgrading pip..."
# pip install --upgrade pip
# if [ $? -ne 0 ]; then
#     echo_error "Failed to upgrade pip."
#     deactivate
#     exit 1
# fi

# # Install dependencies
# if [ -f "$REQUIREMENTS_FILE" ]; then
#     echo_info "Installing dependencies from $REQUIREMENTS_FILE..."
#     pip install -r "$REQUIREMENTS_FILE"
#     if [ $? -ne 0 ]; then
#         echo_error "Failed to install dependencies."
#         deactivate
#         exit 1
#     fi
# else
#     echo_error "$REQUIREMENTS_FILE not found."
#     deactivate
#     exit 1
# fi

# # Run the main script
# if [ -f "$MAIN_SCRIPT" ]; then

#     # Detect if running under Wayland
#     if [ -n "$WAYLAND_DISPLAY" ]; then
#         echo "[INFO] Wayland detected. Setting SDL_VIDEO_X11_FORCE_EGL=1 to force X11 with EGL."
#         export SDL_VIDEO_X11_FORCE_EGL=1
#     else
#         echo "[INFO] Wayland not detected. Proceeding with default settings."
#     fi

#     echo_info "Running $MAIN_SCRIPT..."
#     python "$MAIN_SCRIPT"
#     EXIT_CODE=$?
#     if [ $EXIT_CODE -ne 0 ]; then
#         echo_error "$MAIN_SCRIPT exited with code $EXIT_CODE."
#     fi
# else
#     echo_error "$MAIN_SCRIPT not found."
#     deactivate
#     exit 1
# fi

# # Deactivate the virtual environment
# deactivate
