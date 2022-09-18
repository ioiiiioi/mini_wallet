Run With Python
    Requirements
        - Python 3
        - Django
        - Postgres (either local or cloud)
        - requirements.txt file
        - .env file

    Install
        - if you does not have python3, please download it first from here : https://www.python.org/downloads/
        - this program used Postgre as database.
        - run your virtual environment (Optional)
        - by default this program will run on the port:8000, please make sure your 8000 port isn't used by any application
        - go to program root directory
        - run pip install -r requirements.txt to install python3 library
        - change file name sampleenv to .env
        - run python manage.py seed to populate user table
        - the initial user is "ea0212d3-abd6-406f-8c67-868e814a2436" you'll see the prompt with initial username and email if seed is success.

    Run the program
        - pyhton3 manage.py runserver

        - or you can manipulate the port with your desire 
            e.g. i want to run on port 8001:
                python3 manage.py runserver 8001

Run with Docker compose
    Requirements
         - Docker

    Run the program
        - go to program root directory
        - docker-compose -p mini_wallet -f deployment/docker-compose.yml up -- build
