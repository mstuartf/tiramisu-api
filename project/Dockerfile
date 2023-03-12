FROM python:3.8.5-slim-buster

WORKDIR /app

COPY . .

# install dependencies:
# - psycopg2 for postgres
# - curl, libcurl4-openssl-dev and libssl-dev for celery[sqs]
# - nodejs and npm are required for installing wscat below
# - lsof for debugging sockets
RUN apt-get update \
  && apt-get -y install gcc postgresql \
  && apt-get install -y curl libcurl4-openssl-dev libssl-dev \
  && apt-get install -y nodejs npm lsof \
  && apt-get install libpq-dev \
  && apt-get clean

# wscat for debugging sockets
RUN npm i -g wscat

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install ez_setup
RUN pip install -r requirements.txt

# collect static files
RUN DJANGO_SECRET_KEY="fake-value" python manage.py collectstatic --noinput

# If the absolute path specified in the VOLUME directive is the same as the containerPath specified in the task
# definition, the data in the VOLUME directive path is copied to the data volume.
VOLUME ["/app/static"]

EXPOSE 80

# No CMD because we need this same image for:

# - the migrate one-off task
# - the long-running runserver task
# - the worker tasks

# Instead, commands are defined in the task definition (remote) or docker-compose.yml (local).
