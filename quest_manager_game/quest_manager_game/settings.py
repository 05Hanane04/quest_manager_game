"""
Django settings for Quest Manager Game project.

This is an RPG quest management system where users can manage characters
and complete quests. Configured with PostgreSQL database.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yj+9nsdupp@$a(eb(7fx^*+b4svl)=6$!z0kvuu1&#hd#7ymsi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',          # Django admin site
    'django.contrib.auth',           # Authentication framework
    'django.contrib.contenttypes',   # Content types framework
    'django.contrib.sessions',       # Session framework
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static files management
    'game',                          # Our RPG quest management app
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

ROOT_URLCONF = 'quest_manager_game.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'quest_manager_game.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# ---------------------------------------------------------------------------
# Database Configuration — PostgreSQL
# ---------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'quest_manager',
        'USER': 'root',
        'PASSWORD': '',        # vide par défaut dans XAMPP
        'HOST': 'localhost',
        'PORT': '3307',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Authentication settings
# ---------------------------------------------------------------------------
LOGIN_URL = '/login/'              # Redirect here if not authenticated
LOGIN_REDIRECT_URL = '/dashboard/' # After login, redirect to dashboard
LOGOUT_REDIRECT_URL = '/login/'    # After logout, redirect to login

# ---------------------------------------------------------------------------
# Session settings
# ---------------------------------------------------------------------------
SESSION_COOKIE_AGE = 86400         # Session expires after 24 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ---------------------------------------------------------------------------
# CSRF Trusted Origins (for proxy/reverse-proxy setups)
# ---------------------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    'https://8000-icklwuj19ro54zgrva9in-0ffdc929.us2.manus.computer',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8888'
]

# ---------------------------------------------------------------------------
# Cookie settings for proxy/HTTPS
# ---------------------------------------------------------------------------
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = False

# Trust the X-Forwarded-Proto header from the proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
