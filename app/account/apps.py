# Django
from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'
    label = 'account'

    def ready(self):
        # Load Django signals connection.
        # Based on https://stackoverflow.com/questions/2719038/where-should-signal-handlers-live-in-a-django-project
        from . import signals
