# Good Driver Program - Django Setup

Note - this project was developed for a school project with a team of 5 group members. Their names are listed below:
- John Michael Hayde
- Timothy Morse
- Jason Lyle
- Jacobn Caldwell
- Colin Rogers

## Installation
Must install Django

## Starting Development Server
`python manage.py runserver`\
\
This command will start the web-portal at `localhost` or `yourip:8000`

## App Layout

### portal
Portal is the main web app, handles displaying info and such after login.

### users
Handles the user login and information processing logic.

### Server Requirements and Migrations
`yum install python-devel`\
`yum install mysql-devel`\
`pip install mysqlclient`\
`pip install pillow`\
`pip install django`\
`pip install django-crispy-forms`\
`python3 manage.py makemigrations`\
`python3 manage.py migrate`
