#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Environment setup complete. Activate it using 'source venv/bin/activate'."
