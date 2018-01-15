set IDEA_DATA="IdeaData"
python manage.py import_movies %IDEA_DATA%/movies.tsv
python manage.py import_fields %IDEA_DATA%/Idea_dbo_field_list.tsv
python manage.py import_description %IDEA_DATA%/book_sum.tsv
python manage.py imoprt_person %IDEA_DATA%/book_strans.tsv
python manage.py import_tags %IDEA_DATA%/tags.tsv
python manage.py import_relationship %IDEA_DATA%/book_tags.tsv
python manage.py import_movie_titles %IDEA_DATA%/book_lang.tsv