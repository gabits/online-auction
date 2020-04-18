Online Auction
=======
Back-end application which exposes a REST API for an online auction based on
single user lots (such as eBay).

--------

## Set up instructions
Clone the repository from GitHub. Then, install the application dependencies 
and run the local server.

### Installation
Install dependencies with a Python package manager such as `pip`. 
Preferably, you should do it inside a virtual environment.
```bash
 # From the top-level directory
 pip install -r requirements.txt
```

## Run local server
Run the local Django server. You can specify any ports where you would prefer 
to run it on instead of the default (8000). Be wary to not specify the same
port as the default reserved hosts for other common applications, such as 
database servers or message brokers.
```bash
 python auction/manage.py runserver
 # or
 ./auction/manage.py runserver

 # To run on a different port
 ./auction/manage.py runserver [port_number]
 # e.g. the following example runs on port 80
 ./auction/manage.py runserver 80
```

--------

## Testing
Tests can be ran using Django's usual test command.
```bash
 # Run all test suite for an app
 ./auction/manage.py test [app_name]
# e.g.
 ./auction/manage.py test auction

 # Run individual tests
 ./auction/manage.py test path.to.module

 # For example:
 ./auction/manage.py test auction.api.v1.tests.test_views.TestMockView
```
