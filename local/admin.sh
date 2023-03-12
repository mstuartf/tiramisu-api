#!/bin/bash

# This is a wrapper script to run Django-admin commands inside of the web_svc container.
# It will throw an error if you try to run `migrate`. This should be run by the migrate task (so that
# the local setup is as close to the ECS setup as possible).

if [ $1 = "migrate" ]; then
  printf '%s\n' "You do not need to manually migrate the db; it will run automatically on docker-compose up." >&2
  return
fi

echo "Running python manage.py $* inside of the web_svc container"
docker-compose run --rm web_svc sh -c "python manage.py $*"
