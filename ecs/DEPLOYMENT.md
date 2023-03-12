### Initial setup:
* `aws ecs register-task-definition --cli-input-json file://ecs/task_definitions/web.json`
* `aws ecs create-service --enable-execute-command --cli-input-json file://ecs/services/web.json`

### Deployment

* `. ecs/deploy.sh $NEW_VERSION`

#### Debugging:
* `aws ecs execute-command --cluster td-api --container web --task TASK_ID --interactive --command "/bin/bash"`
* `wscat -c ws://localhost:8001/ws/events/ -x '{"event": $EXAMPLE DATA}'`
