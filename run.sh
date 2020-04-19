#!/bin/bash

export APP_ENVIRONMENT=dev

VIRTUALENV_NAME=online-auction
PORT_NUMBER=8000

update_virtual_environment () {
  source "$(command -v virtualenvwrapper_lazy.sh)"
  workon $VIRTUALENV_NAME
  export PATH=$PATH:${VIRTUAL_ENV}/bin
  pip install --upgrade pip
  pip install -r requirements.txt
  export PYTHONPATH=$PYTHONPATH:$PWD
}

migrate_database() {
  ./app/manage.py migrate
}

start_server() {
  ./app/manage.py runserver ${PORT_NUMBER}
  echo "Server is running on port: ${PORT_NUMBER}"
}

update_virtual_environment
migrate_database
start_server
