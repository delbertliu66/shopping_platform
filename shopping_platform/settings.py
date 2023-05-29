"""
Django settings for shopping_platform project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4(a4+0m5x+jeha&mqs=(lb&0c0le)%^r+0%f8qgt$gx##bar^3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'shopping_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'shopping_platform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',   # 数据库引擎
        'NAME': 'shopping',         # 数据库名，Django不会帮你创建，需要自己进入数据库创建。
        'USER': 'postgres',     # 设置的数据库用户名
        'PASSWORD': '5252',     # 设置的密码
        'HOST': '127.0.0.1',    # 本地主机或数据库服务器的ip
        'PORT': '5432',         # 数据库使用的端口
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 日志配置
import os

LOG_COLORS = {
    'DEBUG': 'light_cyan',
    'INFO': 'purple',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}

LOG_PATH = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] \
            [%(levelname)s]- %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': LOG_COLORS
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(str(BASE_DIR) + '/logs/', 'all.log'),
            'when': 'D',  # this specifies the interval
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 0,  # how many backup file to keep, 10 days
            'formatter': 'colored',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'colored'
        },
        'request_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(str(BASE_DIR) + '/logs/', 'traceback.log'),
            'when': 'D',  # this specifies the interval
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 0,  # how many backup file to keep, 10 days
            'formatter': 'standard',
        },
        'errMsg': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(str(BASE_DIR) + '/logs/', 'errLog.log'),
            'when': 'D',  # this specifies the interval
            'interval': 1,  # defaults to 1, only necessary for other values
            'backupCount': 0,  # how many backup file to keep, 10 days
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'errMsg': {
            'handlers': ['errMsg', 'console'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
