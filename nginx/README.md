Need separate nginx config files for local dev and production. 

To build production nginx image:
* `$ docker build -f nginx/Dockerfile ./nginx -t custom-nginx`
* `$ docker tag custom-nginx:latest public.ecr.aws/q7o3w5k9/custom-nginx:latest`
* `$ docker push public.ecr.aws/q7o3w5k9/custom-nginx:latest`
