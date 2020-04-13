# Python standard
import os

DEBUG = False

# Fail if no SECRET_KEY is provided on a Production environment
SECRET_KEY = os.getenv("SECRET_KEY")
