# Mobile Money Integration
This is a small app to make momo payments and track their status

# Requirements

Python 3.6+
RabbitMQ for background processing

# Project Setup

Create a virtual envrionment with virtualenv env
Create a directory named 'app' inside the env directory that was just created
Clone this repo inside the app directory
Activate your virtual environment (env/scripts/activate)
Do pip install -r requirements.txt

# Migrate Data

Run python manage.py migrate

It will install a sample user (user id = 1) and payments as well

# Run the server

python manage.py runserver localhost:9011

or any port you see fit

# Background Process

Background process is done with Celery, hence the worker and the beat should be fired in separate command prompts of the virtual envrionment.

First, launch the worker by typing the following in the command prompt:

         celery -A app worker -E --concurrency=5 -l debug -P eventlet
         
Then, launch the beat that does periodic task in a separate command prompt:

         celery -A app beat -l debug
         
# Postman

You can import the file  Fenix International.postman_collection.json to postman (V2) and run the requests
