include scripts/commands/vars.mk

## Deletes all containers
docker-remove:
	docker-compose rm -f

## Stops all containers
docker-stop:
	docker-compose stop

## Compiles all the services
docker-build: build
	docker-compose build
	#--no-cache

## Compile and start the service using docker
compose-up: docker-build
	docker-compose up -d

start: compose-up info
	##--scale -d suggester=4 

## Publishes container
docker-publish:
	@scripts/commands/docker-publish.sh


## Execute the service
remove:
	docker stop ${APPNAME}-core
	docker rm ${APPNAME}-core

## Compile and start the service
build:
	@scripts/commands/docker-build.sh

## Compile and start the service using docker
reboot: remove build
	docker run -d --name ${APPNAME}  -p ${SERVER_EXPOSED_PORT}:${SERVER_PORT} ${DOCKER_IMAGE}:${BUILD_TAG}

start-local:
	python app/app.py

mypy:
	mypy app/app.py 

# Installs libraries locally
install:
	pip install -r app/requirements.txt

tests:
	cd app && nosetests -v tests/

info:
	@echo "YO           	         : ${YO}"
	@echo "ServerRoot   	         : ${SERVER_ROOT}"
	@echo "API Base URL 	         : ${SERVER_URL}"
	@echo "API Healthcheck URL       : ${SERVER_URL}/healthcheck"
	@echo "API Healthcheck NGINX URL : http://${SERVER_HOST}:${NGINX_EXPOSED_PORT}/feeds/api/v1/healthcheck"
	@echo "DB connect                : psql -h ${SERVER_HOST} -U ${DATABASE_USER} -p "${DATABASE_PORT}" ${DATABASE_NAME}"
	@echo "SERVER ACCESS             : docker exec -it feeds-core sh"
	@echo "DB ACCESS                 : docker exec -it feeds-db psql -U ${DATABASE_USER} ${DATABASE_NAME}"