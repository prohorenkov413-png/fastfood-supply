import os
from pathlib import Path

# Загружаем переменные окружения из .env файла (для секретных ключей)

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Временные настройки (без .env)
SECRET_KEY = 'django-insecure-temporary-key-for-render'
DEBUG = False
ALLOWED_HOSTS = ['fastfood-supply.onrender.com', 'localhost', '127.0.0.1']

# Настройки перенаправления
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# СЕКРЕТНЫЙ КЛЮЧ (берём из переменных окружения или используем запасной)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

# РЕЖИМ ОТЛАДКИ (В ПРОДАКШНЕ ДОЛЖНО БЫТЬ FALSE!)
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# РАЗРЕШЁННЫЕ ХОСТЫ (укажите ваш домен)
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'fastfood-supply.onrender.com',
    '.onrender.com',  # разрешает все поддомены render.com
]

# Безопасность (Обязательно для продакшна)
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost,http://127.0.0.1').split(',')
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = False  # Включите True если есть SSL-сертификат

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # ДЛЯ СТАТИКИ В ПРОДАКШНЕ
    'django.contrib.staticfiles',
    'shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ОБЯЗАТЕЛЬНО ДЛЯ СТАТИКИ
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fastfood_project.urls'

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
                'shop.context_processors.cart_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'fastfood_project.wsgi.application'

# БАЗА ДАННЫХ (SQLite для простоты, можно поменять на PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ВАЛИДАЦИЯ ПАРОЛЕЙ
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ЛОКАЛИЗАЦИЯ
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ПОДДЕРЖКА ЯЗЫКОВ (русский/английский)
LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
]
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# СТАТИЧЕСКИЕ ФАЙЛЫ (CSS, JS)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ДОПОЛНИТЕЛЬНЫЕ СТАТИЧЕСКИЕ ПАПКИ
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# МЕДИА-ФАЙЛЫ (картинки пользователей)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ПЕРЕНАПРАВЛЕНИЯ
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# EMAIL (настройте для отправки писем)
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@fastfood.ru')

# АВТОМАТИЧЕСКОЕ ПРОЕКТИРОВАНИЕ КЛЮЧА
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'