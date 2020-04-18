# Django
from django.contrib.auth import get_user_model
# Third-party
from django.db.models import signals
from factory import SubFactory, LazyAttribute, LazyAttributeSequence
from factory.django import DjangoModelFactory
from faker import Faker

from common.models import UserProfile

fake = Faker()
auth_user_model = get_user_model()


class AuthUserFactory(DjangoModelFactory):
    id = LazyAttributeSequence(
        lambda _, counter:
        auth_user_model.objects.order_by('id').last().id + counter + 1
        if auth_user_model.objects.exists()
        else counter + 1
    )
    first_name = LazyAttribute(lambda obj: fake.first_name())
    last_name = LazyAttribute(lambda obj: fake.last_name())
    username = LazyAttribute(lambda obj: fake.user_name())
    email = LazyAttribute(lambda obj: fake.email())
    is_staff = False
    is_superuser = False

    class Meta:
        # Get Django's user model without directly referencing the model,
        # according to Django's own recommendations, as the model may change.
        model = auth_user_model
        django_get_or_create = ("username", )


class UserProfileFactory(DjangoModelFactory):
    auth_user = SubFactory(AuthUserFactory)

    class Meta:
        # Get Django's user model without directly referencing the model,
        # according to Django's own recommendations, as the model may change.
        model = UserProfile
        django_get_or_create = ("auth_user", )
