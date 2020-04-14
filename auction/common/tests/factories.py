# Django
from django.contrib.auth import get_user_model

# Third-party
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):

    class Meta:
        # Get Django's user model without directly referencing the model,
        # according to Django's own recommendations, as the model may change.
        model = get_user_model()
