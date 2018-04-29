#!/usr/bin/bash
set -ex
python manage.py create_suggestions
python manage.py lookup_suggestions
python manage.py verify_suggestions
python manage.py lookup_wikidata_props
python manage.py lookup_sitelinks



