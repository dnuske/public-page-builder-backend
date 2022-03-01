"""
Django settings for project project.

"""
import os
import sys
from distutils.util import strtobool
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Application definition
INSTALLED_APPS = [
    'authemail',
    # 'page_builder',
    'page_builder.apps.PageBuilderConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    # 'accounts',
    'corsheaders',
]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'
AUTH_USER_MODEL = 'page_builder.Customer'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

from dotenv import load_dotenv
import os
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT'),
    }
}

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = os.environ.get('STATIC_URL', default='/static/')
STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('STATIC_ROOT', default='static'))

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'EXCEPTION_HANDLER': 'page_builder.error_handling.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
    },
    'USE_SESSION_AUTH': False
}

CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', default=False)
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', default=False)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', default='asd')
ENV_ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')
ALLOWED_HOSTS = ENV_ALLOWED_HOSTS.split(',') if ENV_ALLOWED_HOSTS is not None else []
DEBUG = bool(strtobool(os.environ.get('DEBUG', default='True')))
CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', default='')
if CORS_ALLOWED_ORIGINS:
  CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS.split(',')
else:
  CORS_ALLOWED_ORIGINS = []

APPEND_SLASH=True

ACCOUNT_EMAIL_VERIFICATION='none'
AUTH_EMAIL_VERIFICATION=False

EMAIL_FROM = os.environ.get('AUTHEMAIL_DEFAULT_EMAIL_FROM')
EMAIL_BCC = os.environ.get('AUTHEMAIL_DEFAULT_EMAIL_BCC')

EMAIL_HOST = os.environ.get('AUTHEMAIL_EMAIL_HOST')
EMAIL_PORT = os.environ.get('AUTHEMAIL_EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('AUTHEMAIL_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('AUTHEMAIL_EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


