#!/usr/bin/env bash

# Include colors.sh
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/colors.sh"

docker login ${LOCAL_REGISTRY}

docker tag ${DOCKER_IMAGE_PROXY_COMPOSE} ${LOCAL_REGISTRY}/yapo/${APPNAME}-proxy:${GIT_BRANCH}
docker tag postgres:12.0-alpine ${LOCAL_REGISTRY}/yapo/${APPNAME}-db:${GIT_BRANCH}

docker push ${LOCAL_REGISTRY}/yapo/${APPNAME}-proxy:${GIT_BRANCH}
docker push ${LOCAL_REGISTRY}/yapo/${APPNAME}-db:${GIT_BRANCH}