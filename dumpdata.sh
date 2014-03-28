#!/bin/bash
echo $0: Creating dump
../glossary_env/bin/python manage.py dumpdata --indent=4 main_app auth > ./main_app/fixtures/initial_data.json
echo $0: Creating finished.
