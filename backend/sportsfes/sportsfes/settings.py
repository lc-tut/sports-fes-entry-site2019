"""
Django settings for sportsfes project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from datetime import datetime
try:
    from sportsfes.local_settings import *
except ImportError:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["150.95.213.215"]

CORS_ORIGIN_WHITELIST = (
    'localhost:8080',
)

CORS_ALLOW_CREDENTIALS = True
# Application definition

CSRF_TRUSTED_ORIGINS = (
    'localhost:8080',
)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'user',
    'api',
    'corsheaders',
    'django_apscheduler',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sportsfes.urls'

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

WSGI_APPLICATION = 'sportsfes.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database1',
        'USER': 'database1_role',
        'PASSWORD': 'database1_password',
        'HOST': 'database1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'static')

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'media')

CLIENT_ID = "895653784508-ihj22jtpj3asudcuf51jh0ls3feblsj3.apps.googleusercontent.com"


########## Settings for Email ############
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'cl0wn65536'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#公開するときに、これはコメントアウトすること
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#送信者メールアドレス
FROM_ADDRESS = "hakomori64@gmail.com"
#送信者（団体）名
FROM_NAME = "LinuxClub"

########## 大会に関する設定 ############

# 初心者、経験者混合か
BEGINNER_AND_EXPERIENCED = {
    'Soccer': False,
    'BasketBall': False,
    'Tennis': False,
    'Badminton': False,
    'TableTennis': False,
    'VolleyBall': False
}

# 各競技のエントリー可能最低人数、最大人数
NUMBER_OF_MEMBERS = {
    'Soccer': (7, 13),
    'BasketBall': (5, 10),
    'Tennis': (2, 2),
    'Badminton': (2, 2),
    'TableTennis': (4, 6),
    'VolleyBall': (7, 10)  
}

# 各競技参加チーム数
NUMBER_OF_TEAMS = {
    'Soccer': 16,
    'BasketBall': 18,
    'Tennis': 20,
    'Badminton': 16,
    'TableTennis': 10,
    'VolleyBall': 8
}

# 各競技抽選チーム数
NUMBER_OF_WINNER_TEAMS = {}

for key, value in NUMBER_OF_TEAMS.items():
    NUMBER_OF_WINNER_TEAMS[key] = value * 3 // 4

# 抽選日
DRAWING_LOTS_DATE = datetime(2019, 3, 23, 15, 58)