import os

from .common import *

# Determine current environment
APP_ENVIRONMENT = os.getenv("APP_ENVIRONMENT", "dev")


# Import settings according to current environment.
#
# Following the 12-factor site recommendations (https://12factor.net/),
# these two should have the minimum amount of discrepancies among themselves.
if APP_ENVIRONMENT == "dev":
    from .development import *
elif APP_ENVIRONMENT == "prod":
    from .production import *
