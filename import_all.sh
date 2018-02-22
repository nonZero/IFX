#!/bin/bash
set -e
set -x
./manage.py import_fields_and_tags
./manage.py import_roles
./manage.py import_movies $1/movies.tsv
./manage.py import_description $1/book_sum.tsv
./manage.py import_person $1/book_strans.tsv
./manage.py import_tags $1/tags.tsv
./manage.py import_relationship $1/book_tags.tsv
./manage.py import_movie_titles $1/book_lang.tsv
./manage.py import_strings $1/book_string1.tsv