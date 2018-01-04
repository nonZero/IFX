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

* Import data from tsv files(Tab seperate values):

    movies:
        m import_movies "<folder name>\movies.tsv"
    fields:
        m import_fields "<folder name>\Idea_dbo_field_list.tsv"
    description:
        m import_description "<folder name>\book_sum.tsv"
    tags:
        m import_tags "<folder name>\tags.tsv"
    movie-tag-field relationship:
        m import_relationship "<folder name>\book_tags.tsv"

* Create some sample data:

        python manage.py create_movies 100


* Run your server:

        python manage.py runserver

* Enjoy: 
        
        http://localhost:8000/

# Tips

* Linux/Mac: add to your `.bashrc` or `.bash_profile`:

        alias m='python manage.py'
        alias sp='python manage.py shell_plus'
