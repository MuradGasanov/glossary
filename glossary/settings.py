"""
Django settings for glossary project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '46^ky__p9_w7y@)ot*x=jb*%f0wn1z&-6*k+sxdx_dxj5njv(n'

# SECURITY WARNING: don't run with debug turned on in production!
import socket

if socket.gethostname() in ("murad-P85-D3", "murad-pc"):
    DEBUG = True
else:
    DEBUG = False

ADMINS = (
    ('Murad Gasanov', 'gmn1791@ya.ru'),
)

MANAGERS = ADMINS

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'glossary.apertura.su']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'gunicorn',
    'social_auth',

    'main_app',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)

GOOGLE_OAUTH2_CLIENT_ID = '813279213220-rvslpqbcr6e0qjkucuelsc6lckdv2k7q.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = '6Wuq0-l_EHqoG85SYVCshS-x'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/login_error/'

LOGIN_URL = "/login/"

GOOGLE_WHITE_LISTED_DOMAINS = ['apertura.su', 'oaokrd.ru']

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'main_app.middleware.MiddleWareProcess'
    'social_auth.middleware.SocialAuthExceptionMiddleware'
)

ROOT_URLCONF = 'glossary.urls'

WSGI_APPLICATION = 'glossary.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'glossary',
        'USER': 'glossary',
        'PASSWORD': 'glossary',
        'HOST': '127.0.0.1',
        'PORT': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, '../glossary_static')

STATICFILES_DIRS = (
    'static',
)

TEMPLATE_DIRS = os.path.join(BASE_DIR, 'templates')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}