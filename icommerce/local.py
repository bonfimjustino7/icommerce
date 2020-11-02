from .settings import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DEBUG = True

SECRET_KEY = 't^jy!wtevpe!)ey=29&oi8^p@n+^@s&a=jk@7+u@5xu9_g1oqv'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'icommerce',
        'USER': 'postgres',
        'PASSWORD': 'bonfim',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
