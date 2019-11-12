#!/usr/bin/env bash

# Include colors.sh
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/colors.sh"

echoHeader "Running dependencies script"

set -e
# List of tools used for testing, validation, and report generation
tools=(
    github.com/yapo/socket-mock
    github.com/jstemmer/go-junit-report
    github.com/axw/gocov/gocov
    github.com/AlekSi/gocov-xml
    gopkg.in/alecthomas/gometalinter.v2
)

echoTitle "Installing missing tools"
# Install missed tools
for tool in ${tools[@]}; do
    which $(basename ${tool}) > /dev/null || go get -u -v ${tool}
done

echoTitle "Installing linters"
# Install all available linters
gometalinter.v2 --install

echoTitle "Installing Glide dependencies"
glide install

set +e
