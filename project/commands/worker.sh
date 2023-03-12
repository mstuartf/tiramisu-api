#!/bin/bash -e

# This script is the run command for the worker service
# Don't run with superuser privileges: https://stackoverflow.com/a/59659476/15793866

celery --app=api worker \
       --loglevel=info \
       --uid=nobody \
       --gid=nogroup
