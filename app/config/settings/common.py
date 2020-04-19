# Python standard
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#
#   Application definitions
#
ALLOWED_HOSTS = [
    'localhost',
]

INSTALLED_APPS = [
    #
    #   Django
    #
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #
    #   Third-party
    #
    # REST APIs
    'rest_framework',
    # OAuth 2.0 authentication
    'oauth2_provider',
    # Support cross-domain browser requests for authentication with OAuth
    # coming from external clients
    'corsheaders',
    # Django library to support money calculations and conversions
    'djmoney',

    #
    #   Local apps
    #
    'auction',
    'common',
]

MIDDLEWARE = [
    # CorsMiddleware should be placed as high as possible
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Support cross-origin requests for any requesting client - might not be
# suitable for Production version
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'config.site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

#
#   Database
#
# Point to database committed to this codebase
# TODO: change in the future to an external database host
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

#
#   Password validation
#
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#
#   Internationalization
#
LANGUAGE_CODE = 'en-us'
# Guarantee storage for all dates in times in UTC.
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#
#   Static files (CSS, JavaScript, Images)
#
STATIC_URL = '/static/'

#   REST API settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

#
#   Application data
#
# Default currency used for price calculations and auction; must map to one
# of the django-money supported currencies.
DEFAULT_CURRENCY = "GBP"

# UUID regex to match expected URLs identifiers
UUID_REGEX_FORMAT = (
    "[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}"
)

# OAuth token scheme
OAUTH2_AUTHORIZATION_SCHEME = "Bearer"
