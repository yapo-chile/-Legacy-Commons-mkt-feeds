#!/usr/bin/env bash

# Include colors.sh
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/colors.sh"

echoTitle "Building docker image for ${DOCKER_IMAGE}"
echo "GIT BRANCH: ${BRANCH}"
echo "GIT COMMIT: ${GIT_COMMIT}"
echo "GIT COMMIT SHORT: ${GIT_COMMIT_SHORT}"
echo "BUILD CREATOR: ${BUILD_CREATOR}"
echo "BUILD NAME: ${DOCKER_IMAGE}:${GIT_BRANCH}"

DOCKER_ARGS=" ${DOCKER_ARGS} \
	-t ${DOCKER_IMAGE}:${DOCKER_TAG} \
	-t ${DOCKER_IMAGE}:${COMMIT_DATE_UTC} \
    --label GIT_BRANCH="$BRANCH" \
    --label GIT_COMMIT="$GIT_COMMIT" \
    --label TAG="${DOCKER_IMAGE}:${BUILD_TAG}" \
    --label BUILD_CREATOR="$BUILD_CREATOR" \
    --label VERSION="$VERSION" \
    --label APPNAME="$APPNAME" \
    --build-arg APPNAME="$APPNAME" \
    -f app/dockerfile \
    app/."

echo "args: ${DOCKER_ARGS}"
set -x
docker build ${DOCKER_ARGS}
set +x

echoTitle "Build done"
