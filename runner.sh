#!/bin/bash

# Change to the directory of your Django project
cd /Users/dabolabs/Desktop/dabolabs/SchoolCafeteria

# Activate your virtual environment if you are using one
source /Users/dabolabs/Desktop/dabolabs/dabolabsenv/bin/activate

# Run the Django development server
python manage.py runserver 0.0.0.0:8000 &

# Wait for the server to start (adjust sleep time if needed)
sleep 2

# Open Google Chrome with the URL of your Django project's home page
google-chrome http://127.0.0.1:8000/