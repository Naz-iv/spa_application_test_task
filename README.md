# spa-service

This app was created for managing spa comments from users.

# Create .env before starting

Before running the project either in Docker or locally, you need to create .env file in the project`s root directory.
You can fill it with this data or create it from .env.sample with your own:

`
DJANGO_SECRET_KEY=DJANGO_SECRET_KEY
POSTGRES_HOST=POSTGRES_HOST
POSTGRES_DB=POSTGRES_DB
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
POSTGRES_PORT=POSTGRES_PORT
REDIS_HOST=REDIS_HOST
REDIS_PASSWORD=REDIS_PASSWORD
REDIS_PORT=REDIS_PORT
EMAIL_URL=EMAIL_URL
`

# Project is deployed and can be tested using this link [SPA-APP](https://spa-app-w4bu.onrender.com/)
Please note, debug mode was not disabled to make review process easier. 


# Launching project locally

To launch the application locally, follow next steps:

1. Fork the repository

2. Clone it:
`git clone <here goes the HTTPS link you could copy on github repositiry page>`

3. Create a new branch:
`git checkout -b <new branch name>`

4. Create virtual environment:
`python3 -m venv venv`

5. Acivate venv:
`source venv/Scripts/activate`

6. Install requirements:
`pip3 install -r requirements.txt`

7. Run migrations:
`python3 manage.py migrate`

8. Load the data from fixture:
`python3 manage.py loaddata comments_fixture.json`

9. Run server:
`python3 manage.py runserver`

# Running with docker

If you have Docker Desktop you can simply pull image from Docker Hub:

1. Pull image using shell or bash:
`docker pull nivankiv/spa_application_test_task-app`

2. Run image:
`docker run nivankiv/spa_application_test_task-app`

Alternatively, you cna clone project from git repository and run this commands:
    - docker-compose build
    - docker-compose up

