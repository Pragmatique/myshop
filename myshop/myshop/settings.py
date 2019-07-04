"""
Django settings for myshop project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '89at(j)0d7o%-*_38y!kc+03y#p7^x5+*%0$y!4wi!&f6ie=ro'

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

    'rest_framework',

    'bootstrap3',

    'shop',
    'cart',
    'orders',
    'authproj',
    'paypal.standard.ipn',
    'payment',
    'parler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_EXPIRE_SECONDS = 5*60 #5 minutes


ROOT_URLCONF = 'myshop.urls'

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
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'cart.context_processors.cart',
                'shop.context_processors.products',
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'authproj.User'

LOGIN_REDIRECT_URL='/'
LOGOUT_REDIRECT_URL='/'

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/



#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS=[os.path.join(BASE_DIR, 'locale')]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

LANGUAGES=[
    ('en','English'),
    ('ru','Руский'),
]

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CART_SESSION_ID = 'cart'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#         'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#    )
# }
#
# import datetime
# JWT_AUTH = {
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1/24)
# }

# BRAINTREE_MERCHANT_ID = 'z3tjx3yzjqyq2yf2' # Merchant ID
# BRAINTREE_PUBLIC_KEY = 'zfk2jdmn87bqgddx' # Public Key
# BRAINTREE_PRIVATE_KEY = '475505438af3bfa3652908f323017a23' # Private key

# from braintree import Configuration, Environment
# Configuration.configure(
# Environment.Sandbox,
# BRAINTREE_MERCHANT_ID,
# BRAINTREE_PUBLIC_KEY,
# BRAINTREE_PRIVATE_KEY
# )


PAYPAL_RECEIVER_EMAIL = 'Silchevihor-facilitator@gmail.com'

PAYPAL_TEST = True

PARLER_LANGUAGES = {
    None: (
            {'code': 'en'},
            {'code': 'ru'},
        ),
        'default': {
        'fallback': 'en',
        'hide_untranslated': False,
        }
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

