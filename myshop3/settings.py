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

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'shop',
    'cart',
    'orders',
    'info',
    'mptt',              # https://django-mptt.readthedocs.io/en/latest/index.html
    'easy_thumbnails',   # https://pypi.org/project/easy-thumbnails/
    'django_cleanup',    # https://github.com/un1t/django-cleanup
    'django_summernote', # https://github.com/summernote/django-summernote , https://summernote.org/deep-dive/
    'bootstrap3',        # https://django-bootstrap3.readthedocs.io/en/latest/
    'captcha',           # https://django-simple-captcha.readthedocs.io/en/latest/index.html
    'django.forms',
    'comments',

    'allauth',           # https://django-allauth.readthedocs.io/en/latest/configuration.html
    'allauth.account',
    'allauth.socialaccount',

    'profiles',
    'contacts',
    'newsletter',
    'notifications',    # https://pypi.org/project/django-notifications-hq/#description
    'smart_selects',    # https://github.com/digi604/django-smart-selects

    'cml',              # https://github.com/ArtemiusUA/django-cml
    'import_export',    # https://django-import-export.readthedocs.io/en/latest/installation.html

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware', # Относится к настройке оповещения о битых ссылках
    'debug_toolbar.middleware.DebugToolbarMiddleware', # Использует debug_toolbar
    'cart.middleware.CartMiddleware',

]

ROOT_URLCONF = 'myshop3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'shop/templates/shop'),
                 os.path.join(BASE_DIR, 'shop/templates/shop/error'),
                 os.path.join(BASE_DIR, 'profiles/templates/allauth'),
                 os.path.join(BASE_DIR, 'info/templates'),
                 os.path.join(BASE_DIR, 'contacts/templates'),
                 os.path.join(BASE_DIR, 'newsletter/templates'),
                 #os.path.join(BASE_DIR, 'info/templates/news/custom_field.html'),
		],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.menucategory', # Сквозной вывод бокового левого меню
                'shop.context_processors.filters',      # Сквозной вывод бокового левого фильтра
                'shop.context_processors.bestseller',   # Сквозной вывод бокового левого блока bestseller
                'shop.context_processors.brendlogo',    # Сквозной вывод нижнего блока brend logo
                'shop.context_processors.bestseller',   # Сквозной вывод нижнего блока brend logo
                'shop.context_processors.sale',         # Сквозной вывод нижнего блока sale на главной
                'shop.context_processors.footer',       # Сквозной вывод футера сайта на всех страницах
                'shop.context_processors.price_list',   # Вывод ссылки на загрузку файла прайс-листа в base.html
                'contacts.context_processors.privacy_policy', # Сквозной вывод политики конф. modal_privacy_policy.html

            ],
        },
    },
]

WSGI_APPLICATION = 'myshop3.wsgi.application'


AUTHENTICATION_BACKENDS = (

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

)


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


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

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

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
        'slider': {'size': (300, 300), 'corp':False, 'quality': 99},      # index.html
        'index': {'size': (200, 150), 'corp':True, 'quality': 99},        # index.html
        'akciya': {'size': (200, 150), 'corp':True, 'quality': 99},       # index.html
        'shop': {'size': (200, 150), 'corp':True, 'quality': 99},         # shop.html
        'shop-list': {'size': (200, 150), 'corp':True, 'quality': 99},    # shop-list.html
        'product': {'size': (800, 800), 'corp':True, 'quality': 99},      # product-details.html
        'alb': {'size': (200, 150), 'corp':True, 'quality': 99},          # product-details.html
        'pftc': {'size': (200, 150), 'corp':True, 'quality': 99},         # product-details.html
        'allp': {'size': (200, 150), 'corp':True, 'quality': 99},         # product-details.html
        'cart': {'size': (70, 90), 'corp':True, 'quality': 99},           # cart.html
        'brandlogo': {'size': (100, 100), 'corp':True, 'quality': 99},     # base.html
        'bestsellers': {'size': (100, 100), 'corp':True, 'quality': 99},  # bestseller.html
        'sale': {'size': (100, 100), 'corp':True, 'quality': 99},         # sale.html
        'news': {'size': (190, 130), 'corp':True, 'quality': 99},         # news/list.html
        'compare': {'size': (229, 149), 'corp':True, 'quality': 99},      # shop/compare.html
        #'index_news': {'size': (270, 93), 'corp':True, 'quality': 99},   # index.html
    }
}

THUMBNAIL_SUBDIR = 'thumbs'

# Настройки капчи
# https://django-simple-captcha.readthedocs.io/en/latest/advanced.html
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_IMAGE_SIZE = (150, 50)
CAPTCHA_FONT_SIZE = (28)
CAPTCHA_BACKGROUND_COLOR = '#cccccc'
CAPTCHA_FOREGROUND_COLOR = '#001100'
CAPTCHA_LENGTH = 6

# CAPTCHA_LETTER_ROTATION = (-15, 15)
# CAPTCHA_NOISE_FUNCTIONS = None
# CAPTCHA_BACKGROUND_COLOR = '#ffffff'

#CAPTCHA_OUTPUT_FORMAT = u'%(hidden_field)s%(text_field)s<br>%(image)s'

#FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'


'''
# НАстройки ждя всего проекта
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        # As an example, using Summernote Air-mode
        'airMode': False,
        'width': '90%',
        'height': '300',
        'toolbar': [
            ['style', ['bold', 'italic', 'underline', 'clear']],
             ['font', ['strikethrough', 'superscript', 'subscript']],
             ['fontsize', ['fontsize']],
             ['color', ['color']],
             ['para', ['ul', 'ol', 'paragraph']],
             ['height', ['height']],
        ]


    },
    'disable_attachment': True,
}

'''

# django-allauth
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 5 # Определяет срок действия писем с подтверждением по электронной почте
ACCOUNT_AUTHENTICATION_METHOD = 'username_email' # Вход на сайт по логину и почте
ACCOUNT_EMAIL_VERIFICATION = 'mandatory' # Когда установлено «mandatory», пользователь блокируется от входа, пока адрес электронной почты не будет подтвержден.
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 2 # Количество попыток не удачного ввода логина и пароля. После пользователь блокируется.
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300 # Время блокировки пользователя в секундах после количества не удачного ввода логина и пароля.
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = '/accounts/profile/' # редирект после успешной авторизации
LOGIN_URL = '/accounts/login/'


# НАстройки для django-allauth - добавление своих полей
ACCOUNT_FORMS = {

    'login': 'profiles.forms.SignIn',
    'signup': 'profiles.forms.SignUp',
    # 'add_email': 'allauth.account.forms.AddEmailForm',
    # 'change_password': 'allauth.account.forms.ChangePasswordForm',
    # 'set_password': 'allauth.account.forms.SetPasswordForm',
    # 'reset_password': 'allauth.account.forms.ResetPasswordForm',
    # 'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    # 'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
}

# Настройки вывода сообщений (используется в шаблоне формы обраной связи http://localhost:8001/contact/)
# https://simpleisbetterthancomplex.com/tips/2016/09/06/django-tip-14-messages-framework.html
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

'''Для библиотеки Django Smart Selects, используется в модели Entry'''
USE_DJANGO_JQUERY = True

'''Используется в методе email_send_notify_to_user приложение shop. И в методе control_newsletter_templates в приложении
newsletter'''
site_url = 'http://myshop3.sharelink.ru:8080'

'''Использует debug_toolbar'''
#INTERNAL_IPS = ['192.168.1.5']

'''Синхронизация с 1с, библиотека django-cml, файл cml-pipelines.py'''
CML_PROJECT_PIPELINES = 'myshop3.cml_pipelines'


''' Подгружаем настройки из модуля local_settings.py. '''
try:
    from.local_settings import *
except ImportError:
    pass


DEFAULT_FROM_EMAIL = ''
DOUBLE_ADMIN_EMAIL = ''