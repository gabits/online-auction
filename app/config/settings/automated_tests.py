# Local
from .common import *


#
#   Database
#
# Point to database committed to this codebase
# TODO: change in the future to an external database host
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3')
    }
}

# Set a default randomly generated secret key
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "*9%#$d7$sf3k!g+!d1%%ydm1$@mxe)nss4rt&3!7l&p$1cr&0k"
)
