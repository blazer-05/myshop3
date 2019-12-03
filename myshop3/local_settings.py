import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Разрешенные хосты сайта
ALLOWED_HOSTS = ['myshop3.sharelink.ru', 'www.myshop3.sharelink.ru', 'localhost', '192.168.1.5']  # myshop3.sharelink.ru

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myshop3_db',
	    'USER': 'myshop3user',
        'PASSWORD': 'UserShop305',
        'HOST': 'localhost',
        'PORT': '3306',

    }
}

# используется для отправки админу сообщений о подписке на рассылку (вьюхи subscribe и unsubscribe)
SITES = 'myshop3.sharelink.ru'

# Настройки почтового сервера
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = 'blazer-05@mail.ru'
EMAIL_HOST_PASSWORD = 'P$yopoyOAP21'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'blazer-05@mail.ru' # Основной емейл на который приходят заказы и другие сообщения
DOUBLE_ADMIN_EMAIL = 'atari1971@mail.ru' # Дублирующией емейл на который приходят заказы и другие сообщения
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_USE_TLS = True
#SERVER_EMAIL = 'blazer-05@mail.ru'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
'''
Эта константа DEFAULT_FROM_EMAIL емейл отправителя

во вьюхе это recepients = ['blazer-05@mail.ru'] емейл получателя

Если во вьюхе сделать так recepients = [DEFAULT_FROM_EMAIL] , то емейл отправителя и получателя будет одинаковый
email = EmailMessage('Поступило новое сообщение с сайта №{} от "{}" ' .format(contact.id, full_name), message, DEFAULT_FROM_EMAIL, recepients, admin_recepients)

'''


'''Настройка оповещения об ошибках'''
EMAIL_SUBJECT_PREFIX = 'Привет админ django сайта!'

ADMINS = (
    ('Вадим Полшков', 'blazer-05@mail.ru'),
    ('blazerok', 'atari1971@mail.ru'),
)

'''Настройка оповещения о битых ссылках'''
SEND_BROKEN_LINK_EMAILS = True

MANAGERS = (
    ('Вадим Полшков', 'blazer-05@mail.ru'),
    ('blazerok-05', 'blazer-05@yandex.ua'),
)


