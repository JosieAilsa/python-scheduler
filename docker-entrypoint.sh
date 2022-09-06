#!/bin/bash

cd /opt/hire-challenge/

function __test() {
  echo "Running tests in $(pwd)..."
  pytest
}

function __show_help() {
    echo "Container entrypoint commands:"
    echo "  help - show this help"
    echo "  test - run the tests"
    echo ""
    echo "Any other command will be executed within the container."
}

case ${1} in
  test )
    shift
    __test
    ;;

  help )
    __show_help
    ;;

  * )
    exec "$@"
    ;;
esac
