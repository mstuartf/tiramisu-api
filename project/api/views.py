from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.http import HttpResponse


# This endpoint checks to see if there are any outstanding migrations that need to be run. If so, then this is an ECS
# Task that has just been launched with a new image as part of a deployment and the one-off migration task has not
# finished running. In this case we want the Task to fail the health check so that the old containers continue running
# until the migrations are finished.
# See https://engineering.instawork.com/elegant-database-migrations-on-ecs-74f3487da99f
def health_check(request):
    executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    status = 503 if plan else 200
    return HttpResponse(status=status, content="returning status {}".format(status))
