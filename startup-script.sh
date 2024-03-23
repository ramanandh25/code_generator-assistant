#!/bin/bash

# Install pyenv
echo "Installing pyenv..."
#curl https://pyenv.run | bash

# Set up pyenv in the current shell
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"

# Install build essentials
echo "Installing build essentials..."
sudo apt-get update -y
sudo apt-get install -y build-essential
sudo apt-get -qq -y install vim gcc curl git  libb64-dev software-properties-common

# Install JVM
echo "Installing JVM..."
sudo apt-get install -y default-jre default-jdk

# Install Python 3.10
echo "Installing Python 3.10..."
#pyenv install 3.10.0 -y

# Create virtual environment
echo "Creating virtual environment..."
python3.10 -m venv venv
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

mkdir log_dir

# Run the server
echo "Starting the server..."
uvicorn code_generator.main:app  --host 0.0.0.0 --port 8000 --reload
