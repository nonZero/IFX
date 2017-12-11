# 🎥 IFX 🎥
Israeli film archive

# Setup instructions

* Clone this repo.
* Create a virtualenv:

        mkvirtualenv IFX

* Install requirements:

        pip install -r requirements.txt

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
