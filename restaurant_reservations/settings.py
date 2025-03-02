import os
from pathlib import Path
import environ
import pymysql

pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "CHANGE_ME_TO_A_SECURE_KEY"
DEBUG = True  # Enable for development
ALLOWED_HOSTS = [
    "booking-system-deployment-eda028bd58dc.herokuapp.com",
    "127.0.0.1",
    "localhost",
]

# Add CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://booking-system-deployment-eda028bd58dc.herokuapp.com",
]

# Session and Cookie Settings
SESSION_COOKIE_SECURE = False  # Set to True in production
CSRF_COOKIE_SECURE = False    # Set to True in production
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "reservations",  # our custom app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

ROOT_URLCONF = "restaurant_reservations.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "reservations" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "restaurant_reservations.wsgi.application"

# MySQL
# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

DATABASES = {
    "default": env.db(
        "JAWSDB_URL",  # Use JAWSDB_URL from Heroku
        default="sqlite:///db.sqlite3",  # Fallback for local development
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# For optional password reset emails:
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
