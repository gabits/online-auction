Online Auction
=======
Back-end application which exposes a REST API for an online auction based on
single user lots (such as eBay) placed for sale for a determined period of time.

--------

# Local installation

_Note: Instructions are available for OS X and Linux only._

## Requirements
Ensure you have installed locally the following:
* [Python 3.7.4](https://www.python.org/downloads/release/python-374/)
* [virtualenv](https://pypi.org/project/virtualenv/)
* [virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/)


## Set up

### Automated
Ensure Python 3.7.4 is on your PATH and run:
```bash
 ./setup.sh
``` 

### Manual
Clone the repository from GitHub. Then, install the application dependencies 
and run the local server.

#### App installation
Install dependencies with a Python package manager such as `pip`. 
Preferably, you should do it inside a virtual environment.
```bash
 # From the top-level directory
 pip install -r requirements.txt
```

#### Database
Migrate the database schema.
```bash
 ./app/manage.py migrate
```

## Run local server

#### Automated
```bash
 ./run.sh
```

#### Manual
To run the local Django server manually, use the commands specified below. 
You can specify any ports where you would prefer to run it on instead of the 
default (8000). Be wary to not specify the same port as the default reserved 
hosts for other common applications, such as database servers or message 
brokers.
```bash
 python app/manage.py runserver
 # or
 ./app/manage.py runserver

 # To run on a different port
 ./app/manage.py runserver [port_number]
 # e.g. the following example runs on port 80
 ./app/manage.py runserver 80
```


## Testing
### Manual tests

**Note: Skip this step if you have used the automated set up method.**

#### Load fixtures
To test locally, load seed data to provide testing fixtures. Note that these 
commands should be ran on an empty database, otherwise you may get integrity
errors from data conflicts due to unique fields constraints.
```bash
 ./app/manage.py loaddata account_seed_data.json
 ./app/manage.py loaddata auction_seed_data.json
```

#### Log in
Once that's done, you should have loaded in your database default users. 
Below is the information for admin login:
```bash
 username: admin
 password: tH4wUs81
 # Use the following token in the header like: 
 # "HTTP_AUTHORIZATION: Bearer <token>"
 token: Admin
```
To create more user, use the default admin user provided with seed data, 
go to Django Admin > Authentication and Authorization > Users > Add Users. 
If this does not work or you wish to do it manually, you can run Django's 
management command to create a superuser:
```bash
 ./app/manage.py createsuperuser
``` 

### Automated tests
#### Platform specific
Run tests with the following script:
```bash
 # Execute all tests
 ./test.sh

 # Execute just a module
 ./test.sh path.to.module
 # or
 ./test.sh path/to/module.py
```

#### Using Django
Automated tests for this platform can also be ran using Django's usual test 
command. You must either specify the test settings flag or set an environment 
variable in order to use a dedicated database for testing. 

A dedicated database to run tests is strongly recommended, because otherwise 
tests may find conflicts with data or accidentally flush an existing database 
that was pre-populated.
```bash
 # Run all test suite for an app
 ./app/manage.py test [app_name]
 # e.g.
 ./app/manage.py test auction
 # with settings flag, in case you have not set the env var APP_ENVIRONMENT
 ./app/manage.py test auction --settings=config.settings.automated_tests

 # Run individual tests
 ./app/manage.py test path.to.module

 # For example:
 ./app/manage.py test auction.api.v1.tests.test_views.TestMockView
```
