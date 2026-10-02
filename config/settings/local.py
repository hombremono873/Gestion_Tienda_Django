"""
Configuración de desarrollo. Es la que usa manage.py por defecto.
"""

import os

from dotenv import load_dotenv

from .base import *  # noqa: F401,F403

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Database: PostgreSQL 16 (D-02). Credenciales en secretos/db.env (fuera de Git).

load_dotenv(BASE_DIR / 'secretos' / 'db.env')  # noqa: F405

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Email: los correos (por ejemplo, recuperar contraseña) se muestran en la consola.

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
