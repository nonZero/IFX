# 🎥 IFX 🎥
Israeli film archive

# Setup instructions

* Clone this repo.
* Create a virtualenv:

        mkvirtualenv IFX

* Install requirements:

        pip install -r requirements.txt

* Connecting to PostgreSQL after installing

    1 - open the SQL shell(plsl)
        if the installation was with default values - press Enter until the password and enter the one you've logged in the installation.
    2 - after logging in type with the semicolons:

        create user ifx;
        \password ifx;

        - type the password :

            'ifx@DB'

        (and re-enter it.)

        create database ifx owner ifx;

    and that's it.

* Create tables:

        python manage.py migrate

* Create some sample data:

        python manage.py create_movies 100


* Run your server:

        python manage.py runserver

* Enjoy: 
        
        http://localhost:8000/

* Import data (Tab seperate values):

        python manage.py import_movies idea_data/movies.tsv
        python manage.py import_tags idea_data/tags.tsv
        python manage.py import_relationship idea_data/book_tags.tsv

# Tips

* Linux/Mac: add to your `.bashrc` or `.bash_profile`:

        alias m='python manage.py'
        alias sp='python manage.py shell_plus'
