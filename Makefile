include scripts/commands/vars.mk
-include scripts/commands/secrets.mk

export BRANCH ?= $(shell git branch | sed -n 's/^\* //p')
export COMMIT_DATE_UTC ?= $(shell TZ=UTC git show --quiet --date='format-local:%Y%m%d_%H%M%S' --format="%cd")

export DOCKER_TAG ?= $(shell echo ${BRANCH} | tr '[:upper:]' '[:lower:]' | sed 's,/,_,g')
export CHART_DIR ?= k8s/${APPNAME}


## Deletes all containers
docker-remove: docker-stop
	docker-compose rm -f

## Stops all containers
docker-stop:
	docker-compose stop

## Push gateway and db images to local registry
docker-push-local:
	@scripts/commands/docker-local-registry.sh

## Compiles all the services
docker-build: build build-proxy
	docker-compose build --no-cache

## Compile and start the service using docker
compose-up: docker-build
	docker-compose up -d

start: compose-up info
	##--scale -d core=4 

## Publishes container
docker-publish:
	@scripts/commands/docker-publish.sh

## Publishes container in local registry
docker-publish-local:
	@scripts/commands/docker-local-registry.sh

## Upload helm charts for deploying on k8s
helm-publish:
	@echo "Publishing helm package to Artifactory"
	helm lint ${CHART_DIR}
	helm package ${CHART_DIR}
	jfrog rt u "*.tgz" "helm-local/yapo/" || true

## Execute the service
remove:
	docker stop ${APPNAME}-core
	docker rm ${APPNAME}-core

## Compile and start the service
build:
	@scripts/commands/docker-build.sh

## Compile and start proxy service
build-proxy:
	@scripts/commands/docker-build-proxy.sh

## Compile and start the service using docker
reboot: remove build
	docker run -d --name ${APPNAME} -p ${SERVER_EXPOSED_PORT}:${SERVER_PORT} ${DOCKER_IMAGE}:${BUILD_TAG}

# Starts app locally
start-local:
	python app/app.py

# Run typing tests
mypy:
## Requires mypy
	mypy app/app.py

# Installs libraries locally
install:
	pip install -r app/requirements.txt

# Run tests
test:
## Requires nose
	cd app && nosetests -v tests/

# Run codestyle lint
## Requires pycodestyle
check-style:
	pycodestyle app/

# Run code pep8 formater
## requires autopep8
auto-format:
	autopep8 --in-place --aggressive --aggressive -r app/

# Run pylint code static checker
## requires pylint
pylint:
	pylint app/*.py app/**/*.py

## Run lints to generate report
lints:
	@scripts/commands/lints.sh

## runs all related test to check app
tests: check-style lints

## Starts gunicorn locally simulating a dockerized enviroment
gunicorn:
	cd app && gunicorn -b ${SERVER_HOST}:${SERVER_PORT} --log-level=debug --enable-stdio-inheritance --preload --capture-output app:APP

## shows app info
info:
	@echo "Service: ${APPNAME}"
	@echo "Images from latest commit:"
	@echo "- ${DOCKER_IMAGE}:${DOCKER_TAG}"
	@echo "- ${DOCKER_IMAGE}:${COMMIT_DATE_UTC}"
	@echo "API Base URL: ${BASE_URL}"
	@echo "Healthcheck: curl ${BASE_URL}/healthcheck"
	@echo "API Healthcheck NGINX URL : http://${SERVER_HOST}:${NGINX_EXPOSED_PORT}/feeds/api/v1/healthcheck"
	@echo "DB connect                : psql -h ${SERVER_HOST} -U ${DATABASE_USER} -p "${DATABASE_PORT}" ${DATABASE_NAME}"
	@echo "SERVER ACCESS             : docker exec -it feeds-core sh"
	@echo "DB ACCESS                 : docker exec -it feeds-db psql -U ${DATABASE_USER} ${DATABASE_NAME}"