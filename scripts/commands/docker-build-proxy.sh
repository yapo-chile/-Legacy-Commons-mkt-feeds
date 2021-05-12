#!/usr/bin/env bash

# Include colors.sh
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/colors.sh"

#Build code again now for docker platform
echoHeader "Building code for docker platform"

set +e

echoTitle "Starting Docker Engine"
if [[ $OSTYPE == "darwin"* ]]; then
    echoTitle "Starting Mac OSX Docker Daemon"
    $DIR/docker-start-macosx.sh
elif [[ "$OSTYPE" == "linux-gnu" ]]; then
    echoTitle "Starting Linux Docker Daemon"
    sudo start-docker-daemon
else
    echoError "Platform not supported"
fi


echoTitle "Building docker image for ${DOCKER_IMAGE}-proxy"
echo "GIT BRANCH: ${BRANCH}"
echo "GIT COMMIT: ${GIT_COMMIT}"2
echo "GIT COMMIT SHORT: ${GIT_COMMIT_SHORT}"
echo "BUILD CREATOR: ${BUILD_CREATOR}"
echo "BUILD NAME: ${DOCKER_IMAGE}:${DOCKER_TAG}"

DOCKER_ARGS=" -t ${DOCKER_IMAGE}-proxy:${DOCKER_TAG} \
    -f nginx/dockerfile \
    ."

echo "args: ${DOCKER_ARGS}"
set -x
docker build ${DOCKER_ARGS}
set +x

echoTitle "Build done"
