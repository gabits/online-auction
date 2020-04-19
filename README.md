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

### Run local server
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
 ./app/manage.py runserver 80
```

--------

## Testing
### Manual tests
To test locally, load seed data to provide testing fixtures. Note that this 
command should be ran on an empty database, otherwise you may get integrity
errors from data conflicts due to unique fields constraints.
```bash
 ./app/manage.py loaddata seed_data.json
```
Once that's done, you should have loaded in your database the default user 
information for login and API requests:
```bash
 username: admin
 password: testtest
 token: 1234
```
To create more user, use the default admin user provided with seed data, 
go to Django Admin > Authentication and Authorization > Users > Add Users. 
If this does not work or you wish to do it manually, you can run Django's 
management command to create a superuser:
```bash
 ./app/manage.py createsuperuser
``` 

### Automated tests
Automated tests for this platform can be ran using Django's usual test command.
```bash
 # Run all test suite for an app
 ./app/manage.py test [app_name]
# e.g.
 ./app/manage.py test auction

 # Run individual tests
 ./app/manage.py test path.to.module

 # For example:
 ./app/manage.py test auction.api.v1.tests.test_views.TestMockView
```
`