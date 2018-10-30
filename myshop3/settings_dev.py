"""
Django settings for myshop3 project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/

"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*4tn&e7_af55ix$xe##57k@*ksl!7%(kdw!*0gxt&bo25z_5#)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['myshop3.sharelink.ru', 'localhost']  # myshop3.sharelink.ru


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'cart',
    'orders',
    'mptt',            # https://django-mptt.readthedocs.io/en/latest/index.html
    'easy_thumbnails', # https://pypi.org/project/easy-thumbnails/
    'django_cleanup',  # https://github.com/un1t/django-cleanup
    'django_summernote', # https://github.com/summernote/django-summernote
    'bootstrap3',
    'rest_framework',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cart.middleware.CartMiddleware',
]

ROOT_URLCONF = 'myshop3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'shop/templates'),
		],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.menucategory', # Сквозной вывод бокового левого меню
                'shop.context_processors.filters', # Сквозной вывод бокового левого фильтра
                'shop.context_processors.bestseller', # Сквозной вывод бокового левого блока bestseller
                'shop.context_processors.brendlogo', # Сквозной вывод нижнего блока brend logo
                #'shop.context_processors.base', # Сквозной вывод нижнего блока brend logo
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
	    'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static_dev'),
)

# # Настройка вывода дерева категорий 10 веток https://django-mptt.readthedocs.io/en/latest/index.html
# MPTT_ADMIN_LEVEL_IDENT = 100

# Настройки миниатюр для изображений https://pypi.org/project/easy-thumbnails/
THUMBNAIL_ALIASES = {
    '': {
        'slider': {'size': (500, 200), 'quality': 99},                  # index.html
        'index': {'size': (200, 150), 'corp':True, 'quality': 99},      # index.html
        'akciya': {'size': (200, 150), 'corp':True, 'quality': 99},     # index.html
        'shop': {'size': (200, 150), 'corp':True, 'quality': 99},       # shop.html
        'shop-list': {'size': (200, 150), 'corp':True, 'quality': 99},  # shop-list.html
        'alb': {'size': (200, 150), 'corp':True, 'quality': 99},        # product-details.html
        'pftc': {'size': (200, 150), 'corp':True, 'quality': 99},       # product-details.html
        'allp': {'size': (200, 150), 'corp':True, 'quality': 99},       # product-details.html
        'cart': {'size': (70, 90), 'corp':True, 'quality': 99},         # cart.html
        'brandlogo': {'size': (200, 82), 'corp':True, 'quality': 99},   # base.html
    }
}