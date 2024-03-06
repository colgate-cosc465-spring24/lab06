#/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./docker_traceroute.sh DESTINATION"
    exit 1
fi

DESTINATION=$1

docker run --tty --interactive --rm --name=${USER}_traceroute agemberjacobson/cosc465traceroute:latest paris-traceroute $DESTINATION
