# Setting up development environment

1. git clone https://github.com/DarshanKappa/Stack_Overflow_API.git
2. install virtual environment `pip install virtualenv`
3. create a virtual environment `python -m virtualenv .env`
4. activate the virtual environment
5. pip install -r requirement.txt

##  Setup Database
6. Install and setup Postgres in your machine
7. Create a new database (stack_overflow_db)

## Settting up migrations
8. `python manage.py makemirations`
9. `python manage.py migrate`

##  Run the project
10. `python manage.py runserver`