#!/bin/bash -e

# This script is the run command for the web service.
# Allow optional args to be passed to support live-reloading when running locally.

gunicorn api.wsgi --bind=0.0.0.0:8000 --timeout 90 $@
