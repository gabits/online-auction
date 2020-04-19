# Django
from django.urls import path, re_path
from django.conf import settings

# Local
from account.api.v1 import views

app_name = 'v1'

urlpatterns = [
    path(
        'users/me/',
        views.MyUserProfileRetrieveAPIView.as_view(),
        name="user_list"
    ),
    path(
        'users/',
        views.UserProfileListAPIView.as_view(),
        name="user_list"
    ),
    re_path(
        f'^users/(?P<public_id>{settings.UUID_REGEX_FORMAT})$',
        views.UserProfileRetrieveAPIView.as_view(),
        name="user_detail"
    ),
]
