# 🎥 IFX 🎥
Israeli film archive

# Requirements

* [postgres](https://github.com/nonZero/setups/blob/master/postgres-setup.md)
* [pipenv](http://pipenv.readthedocs.io/en/latest/)

# Setup instructions

* Clone this repo.
* `pipenv install`
* Assuming your user can create DBs:

        python manage.py sqlcreate

* Create tables:

        python manage.py migrate

* Import data from dump (not published yet on github):

        python manage.py loaddata all_data.json

* Run your server:

        python manage.py runserver

* Enjoy: 
        
        http://localhost:8000/

# Tips

* Linux/Mac: add to your `.bashrc` or `.bash_profile`:

        alias m='python manage.py'
        alias sp='python manage.py shell_plus'
