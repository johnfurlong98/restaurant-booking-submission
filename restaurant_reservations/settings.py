import os
from pathlib import Path
import environ
import pymysql
pymysql.install_as_MySQLdb()


# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

JAWSDB_URL="mysql://mebl1wnhamn7inwn:yol5w10i95vat85h@zwgaqwfn759tj79r.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/lujrf9ah5otba4i7"

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'CHANGE_ME_TO_A_SECURE_KEY'
DEBUG = True  # Turn off in production
ALLOWED_HOSTS = ['booking-system-deployment-eda028bd58dc.herokuapp.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reservations',  # our custom app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restaurant_reservations.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'reservations' / 'templates'],
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

WSGI_APPLICATION = 'restaurant_reservations.wsgi.application'

# MySQL
DATABASES = {
    'default': env.db(
        'JAWSDB_URL',
        default='sqlite:///db.sqlite3'
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# For optional password reset emails:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
