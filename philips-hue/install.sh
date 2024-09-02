#!/bin/bash

echo "Starting installation..."

echo "Creating and activating a virtual environment (since pip cannot be used directly in newer versions of Raspberry Pi OS)..."
sudo apt install python3-venv -y

if [ $? -ne 0 ]; then
    echo "Failed to install python3-venv. Exiting..."
    exit 1
fi

echo "Creating virtual environment (might take a while)..."
python3 -m venv unix-gradient-philips-hue

if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment. Exiting..."
    exit 1
fi

echo "Virtual environment 'unix-gradient-philips-hue' created."

echo "Activating virtual environment..."
source unix-gradient-philips-hue/bin/activate

if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment. Exiting..."
    exit 1
fi

echo "Virtual environment activated."

echo "Installing necessary libraries..."
pip install requests

if [ $? -ne 0 ]; then
    echo "Failed to install necessary libraries. Exiting..."
    exit 1
fi

echo "Necessary libraries installed."

echo "Installation complete."
