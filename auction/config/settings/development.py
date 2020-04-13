import os

DEBUG = True

# Set a default randomly generated secret key
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "btwh9fi63zd)wp&cw5ha^hq0l1f4*8g!px-z#7jms+))+xk=y@"
)
