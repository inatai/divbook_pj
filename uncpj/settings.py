from email.policy import default
from pathlib import Path
import os
from decouple import config
from dj_database_url import parse as dburl
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

from socket import gethostname
hostname = gethostname()

# 本番環境
DEBUG = False

import dj_database_url
db_from_env = dj_database_url.config()

DATABASES = {
    'default': dj_database_url.config()
}

ALLOWED_HOSTS = [
    'divbook.herokuapp.com',
    'https://divbook.herokuapp.com/',
    'localhost',
    'www.localhost',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.apps.AppConfig',
    'accounts.apps.AccountsConfig',
    'widget_tweaks',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'uncpj',
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

ROOT_URLCONF = 'uncpj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'uncpj.wsgi.application'




# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = str(BASE_DIR / 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICAITON = 'none'


AUTH_USER_MODEL = 'accounts.CustomUser'
ACCOUNT_AUTHENTICATION_METHOD = 'email' # 認証方法をメールアドレスにする
ACCOUNT_USER_MODEL_USERNAME_FIELD = None # Userモデルにusernameは無い
ACCOUNT_EMAIL_REQUIRED = True # メールアドレスを要求する
ACCOUNT_USERNAME_REQUIRED = False # ユーザー名を要求しない

X_FRAME_OPTIONS = 'SAMEORIGIN'#iframeを表示させるための設定

try:
    from .local_settings import *
except ImportError:
    pass

# Debug=Falseの時だけ実行する設定
if not DEBUG:
    SECRET_KEY = os.environ['SECRET_KEY'] 
    import django_heroku
    django_heroku.settings(locals())