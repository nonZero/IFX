#!/bin/bash
set -e
set -x
./manage.py import_movies $1/movies.tsv
./manage.py import_fields $1/Idea_dbo_field_list.tsv
./manage.py import_description $1/book_sum.tsv
./manage.py imoprt_person $1/book_strans.tsv
./manage.py import_tags $1/tags.tsv
./manage.py import_relationship $1/book_tags.tsv
./manage.py import_movie_titles $1/book_lang.tsv