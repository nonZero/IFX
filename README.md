# IFX
Israeli film archive

# 🎥 Setup instructions 🎥

* Clone this repo.
* Create a virtualenv:

        mkvirtualenv cinamatheque

* Install requirements:

        pip install -r requirements.txt

* Create tables:

        python manage.py migrate

* Create some sample data:

        python manage.py create_movies 100


* Run your server:

        python manage.py runserver

* Enjoy: http://localhost:8000/

# Tips

* Linux/Mac: add to your `.bashrc` / `.bash_profile`:

    alias m='python manage.py'
    alias sp='python manage.py shell_plus'
