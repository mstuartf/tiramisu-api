#!/bin/bash -e

PREV=$(tail -n 1 ecs/VERSIONS)

read -p "The last version was $PREV. What is the next version?" NEXT

echo "updating $PREV to $NEXT"

# replace the version number in all task def files
sed -i '' "s/$PREV/$NEXT/g" ecs/task_definitions/web.json
sed -i '' "s/$PREV/$NEXT/g" ecs/task_definitions/worker.json
sed -i '' "s/$PREV/$NEXT/g" ecs/task_definitions/migrate.json

# Build new image and push to ECR:
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 112991276079.dkr.ecr.eu-west-2.amazonaws.com
docker build -t td-api ./project
docker tag td-api td-api:$NEXT
docker tag td-api:$NEXT 112991276079.dkr.ecr.eu-west-2.amazonaws.com/td-api:$NEXT
docker push 112991276079.dkr.ecr.eu-west-2.amazonaws.com/td-api:$NEXT

# Update date the image in the task def files and update ECS task defs:
aws ecs register-task-definition --cli-input-json file://ecs/task_definitions/web.json --no-cli-pager
aws ecs register-task-definition --cli-input-json file://ecs/task_definitions/worker.json --no-cli-pager
aws ecs register-task-definition --cli-input-json file://ecs/task_definitions/migrate.json --no-cli-pager

# Run the migrations if any required:
aws ecs run-task --no-cli-pager --cluster td-api --task-definition td-api-migrate --count 1 --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[subnet-0e229b2922ab21cce],securityGroups=[sg-0f3fd09a5e7aa66ea],assignPublicIp=ENABLED}"

# Update the services (they will automatically point to the latest task def):
aws ecs update-service --no-cli-pager --region eu-west-2 --cluster td-api --service td-api-web-2 --task-definition td-api-web
aws ecs update-service --no-cli-pager --region eu-west-2 --cluster td-api --service td-api-worker --task-definition td-api-worker

# Add this version to the list
echo $NEXT >> ecs/VERSIONS

echo "finished deploying $NEXT"
