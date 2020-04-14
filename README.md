Online Auction
=======
Back-end application which exposes a REST API for an online auction based on
single user lots (such as eBay).

--------

## Installation
Install dependencies with a Python package manager such as `pip`. 
Preferably, you should do it inside a virtual environment.
```bash
 # From the top-level directory
 pip install ./requirements.txt
```

--------

## Testing
Tests can be ran using Django's usual test command.
```bash
 # Run all test suite
 ./auction/manage.py test

 # Run individual tests
 ./auction/manage.py test path.to.module

 # For example:
 ./auction/manage.py test auction.api.v1.tests.test_views.TestMockView
```
