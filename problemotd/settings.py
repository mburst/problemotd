"""
Django settings for problemotd project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

ENVIRONMENT = os.environ
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENVIRONMENT.get(
    "SECRET_KEY", "_a+u72oii#)9p%&l4!@z66_815e1c7(7j892&k_oxjqoxxpq=9"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(ENVIRONMENT.get("DEBUG", True))

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

ADMINS = (("Max", ENVIRONMENT.get("EMAIL_USER")),)

# Application definition

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "core",
    "djrill",
    "compressor",
    "social_django",
    #'debug_toolbar',
)

MIDDLEWARE = (
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    "django.middleware.cache.FetchFromCacheMiddleware",
)

ROOT_URLCONF = "problemotd.urls"

WSGI_APPLICATION = "problemotd.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "problemotd",
            "USER": "postgres",
            "PASSWORD": "password",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }
else:
    import dj_database_url

    DATABASES = {"default": dj_database_url.config()}
    ALLOWED_HOSTS = [".problemotd.com"]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
# COMPRESS_OFFLINE = True
COMPRESS_ENABLED = False
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

# Honeypot BlackList
HTTPBL_KEY = ENVIRONMENT.get("HTTPBL_KEY")
HTTPBL_ADDRESS = "dnsbl.httpbl.org"
HTTPBL_TL = 45  # Threat Level

MANDRILL_API_KEY = ENVIRONMENT.get("MANDRILL_API_KEY", "")
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
SERVER_EMAIL = "no-reply@problemotd.com"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Authentication
AUTHENTICATION_BACKENDS = (
    "social_core.backends.github.GithubOAuth2",
    #'social_core.backends.contrib.bitbucket.BitbucketBackend',
    "django.contrib.auth.backends.ModelBackend",
)

GITHUB_APP_ID = ENVIRONMENT.get("GITHUB_APP_ID", "")
GITHUB_API_SECRET = ENVIRONMENT.get("GITHUB_API_SECRET", "")
GITHUB_EXTENDED_PERMISSIONS = ["user:email"]
# BITBUCKET_CONSUMER_KEY = ENVIRONMENT.get('BITBUCKET_CONSUMER_KEY', '')
# BITBUCKET_CONSUMER_SECRET = ENVIRONMENT.get('BITBUCKET_CONSUMER_SECRET', '')

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGIN_ERROR_URL = "/login/"

SOCIAL_AUTH_DEFAULT_USERNAME = "Problem Master"
SOCIAL_AUTH_UUID_LENGTH = 8
SOCIAL_AUTH_FORCE_POST_DISCONNECT = True
SOCIAL_AUTH_SANITIZE_REDIRECTS = False
SOCIAL_AUTH_URL_NAMESPACE = "social"

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_user",
    #'social_auth.backends.pipeline.associate.associate_by_email',
    "core.user.get_username",
    "core.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)
# INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

try:
    from local_settings import *
except ImportError:
    pass
