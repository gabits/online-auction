#!/bin/bash

export APP_ENVIRONMENT=test

PYTHON_PATH=`which python3.7`
VIRTUALENV_NAME=online-auction-test
PROJECT_NAME=app

VERBOSITY=3
TEST_APPS="auction common"

#
#   Discover test modules
#
# Accept a test modules argument to run only specified tests.
TEST_MODULES=${1%.py}
# Ensure we only run test modules for this project
TEST_MODULES=${TEST_MODULES#*$PROJECT_NAME/}
# Convert from Unix path to Python path, if not already provided as such.
TEST_MODULES=${TEST_MODULES//\//.}


create_virtual_environment () {
  mkvirtualenv $VIRTUALENV_NAME --python=$PYTHON_PATH
}


install_dependencies () {
  # Deactivate any currently active virtual environment
  deactivate
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


setup_test_database() {
  rm ./app/config/databases/test_db.sqlite3
  python ./app/manage.py migrate
}


run_tests() {
  if [[ -z "${TEST_MODULES}" ]] ; then
     echo "Running all tests for online-auction /app/ project."
     python ./app/manage.py test ${TEST_APPS} -v ${VERBOSITY} --settings=config.settings.automated_tests
  else
     echo "Running only specified test modules: ${SPECIFIED_TEST}."
     python ./app/manage.py test ${TEST_MODULES} -v ${VERBOSITY} --settings=config.settings.automated_tests
  fi
}


install_dependencies
setup_test_database
run_tests
# Deactivate virtual environment
deactivate
