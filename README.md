# ABOUT

# STRUCTURE

* `project` contains all of the application code, Dockerfile to build the image and the different container commands for
web, worker and migrate instances (these commands are used by docker-compose locally and in the ECS Task Definitions).
* `ci` contains the scripts used by the GitLab pipeline to build and deploy the application to ECS.

# DEPLOYMENT

* The `deploy` stage of this repo's pipeline triggers a downstream job in the [Deployment Manager](https://gitlab.com/tactillo/ecosystem/deployment/deployment-manager) repo (via the
  [Deployment Throttler](https://gitlab.com/tactillo/ecosystem/deployment/deployment-throttler) to prevent overlapping deployments). See the [Deployment](https://gitlab.com/tactillo/ecosystem/deployment)
  subgroup on GitLab and [this SO question](https://stackoverflow.com/c/tactillo/questions/68) for more info.

## MAKING CHANGES

If you make changes to the structure, always test that the following still work:
* Building the docker image: `$ cd project/ && docker build --no-cache .`
* Building and running locally using compose: `$ docker-compose build --no-cache` / `docker-compose up`
* Creating migration files: `$ . local/admin.sh makemigrations`

## DOCKER ISSUES

* `You don't have enough free space in /var/cache/apt/archives/`
--> Run `$ docker system prune`

# LOCAL SETUP

## PYCHARM

* To ensure imports are resolved: right-click the `project` dir and select `Mark Directory as > Sources Root`.
* To ensure PyCharm understands Django syntax: go to `Preferences > Languages & Frameworks > Django > Enable Django Support`.

## ENVIRONMENT VARIABLES

* Create a `.env` file from the `template.env` file: `$ cp local/template.env local/.env`.
* This file will be used to set environment variable values inside the local containers. Populate with desired values.
* This file will be gitignored.
* Setup pre-commit hooks for [Black](https://github.com/psf/black):
  `$ echo "docker-compose -f ./pre-commit/docker-compose.yml run pre-commit" > .git/hooks/pre-commit`
  `$ chmod +x .git/hooks/pre-commit`

## DOCKER

* Make sure you have Docker and docker-compose installed on your machine.
* To build the app images, run `$ docker-compose build`.
* To start the app containers, run `$ docker-compose up` and access the api at `http://127.0.0.1:1337`.
* To inspect the db, run `docker container exec -it api_postgres_svc_1 psql postgres postgres thisisapassword`
* Run `django-admin` commands (e.g. `makemigrations`, `createsuperuser`, `collectstatic`) inside the web_svc
  container using `local/admin.sh` (e.g. `. local/admin.sh createsuperuser`).
* Run `docker-compose -f docker-compose.test.yml up` to run the test suite (can't use
  the admin script for this because it also depends on the Elasticsearch container).

## DATA

To load a starter db dump:
* Follow the [instructions](https://stackoverflow.com/c/tactillo/questions/88/89#89) for exporting a remote DB dump.
* Run your web service locally: `$ docker-compose run web_svc bash`
* Load the file into your local postgres service: `$ psql -h postgres_svc -U postgres -d postgres -f dumps/starter.sql`
* You will need the postgres password set in `.env` in the steps above.

# Static files

* Static files are generated in the `Dockerfile` (see the `collectstatic` command) so you need to rebuild if
  there are any changes.
* Locally, they are shared with the `nginx` container via the `static_volume`.
* Remotely, they are shared with the `nginx` container using [bind mounts](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/bind-mounts.html):

> You can define one or more volumes on a container, and then use the volumesFrom parameter in a different container
  definition (within the same task) to mount all of the volumes from the sourceContainer at their originally defined
  mount points. The volumesFrom parameter applies to volumes defined in the task definition, and those that are built
  into the image with a Dockerfile.

* The commit for these changes in the Environment Deployer repo is [here](https://gitlab.com/tactillo/ecosystem/deployment/environment-deployer/-/commit/1dbb782af60cf7ee57646cc1e7c888b2407667a5).

# File uploads to S3

Some of the `Ops` endpoints require file uploads to S3. We use [pre-signed URLs](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html)
for this.

Since we are not using volumes for localstack, you will need to create the following buckets to work on this locally:
* `$ . local/s3.sh`
