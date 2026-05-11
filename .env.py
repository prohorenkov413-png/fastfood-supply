# Django Secret Key (сгенерируйте свой!)
DJANGO_SECRET_KEY=django-insecure-your-unique-secret-key-here-12345

# Режим отладки (False для продакшна)
DEBUG=False

# Разрешённые хосты (через запятую без пробелов)
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com,www.yourdomain.com

# CSRF доверенные источники
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1,https://yourdomain.com

# Email настройки (если используете)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com