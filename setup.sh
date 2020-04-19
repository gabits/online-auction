#!/bin/bash

export APP_ENVIRONMENT=dev
PYTHON_PATH=`which python3.7`
VIRTUALENV_NAME=online-auction


create_virtual_environment () {
  rmvirtualenv $VIRTUALENV_NAME
  mkvirtualenv $VIRTUALENV_NAME --python=$PYTHON_PATH
}


install_dependencies () {
  source "$(command -v virtualenvwrapper_lazy.sh)"
  export PATH=$PATH:/usr/local/bin
  create_virtual_environment
  export PATH=$PATH:${VIRTUALENV_NAME}/bin
  export PYTHONPATH=$PYTHONPATH:$PWD
  workon $VIRTUALENV_NAME
  pip install --upgrade pip
  pip install -r requirements.txt
  deactivate
  workon $VIRTUALENV_NAME
}


migrate_database() {
  echo "Running migrations"
  ./app/manage.py migrate
  echo "Migrations finished."
}

load_initial_data() {
  echo "Loading initial application data."
  ./app/manage.py loaddata seed_data.json
  echo "Finished loading seed data."
}

install_dependencies
migrate_database
load_initial_data
