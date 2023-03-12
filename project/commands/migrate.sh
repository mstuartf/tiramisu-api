#!/bin/bash -e

# This script is the run command for the one-off migration task

python manage.py migrate
