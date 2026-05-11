#!/usr/bin/env python
# prepare_deploy.py - запустить перед публикацией

import os
import subprocess
import sys

def run_command(cmd):
    print(f">>> {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    print("=" * 50)
    print("🚀 ПОДГОТОВКА ПРОЕКТА К ПУБЛИКАЦИИ")
    print("=" * 50)
    
    # 1. Проверка наличия .env файла
    if not os.path.exists('.env'):
        print("\n⚠️ Файл .env не найден!")
        print("Создайте его из шаблона .env.example")
        return
    
    # 2. Установка зависимостей
    print("\n📦 Установка зависимостей...")
    run_command("pip install -r requirements.txt")
    
    # 3. Сбор статических файлов
    print("\n📁 Сбор статических файлов...")
    run_command("python manage.py collectstatic --noinput")
    
    # 4. Создание миграций
    print("\n📝 Создание миграций...")
    run_command("python manage.py makemigrations")
    
    # 5. Применение миграций
    print("\n🗄️ Применение миграций...")
    run_command("python manage.py migrate")
    
    # 6. Создание суперпользователя (интерактивно)
    print("\n👑 Создание суперпользователя...")
    run_command("python manage.py createsuperuser")
    
    print("\n" + "=" * 50)
    print("✅ ПОДГОТОВКА ЗАВЕРШЕНА!")
    print("=" * 50)
    print("\n📋 Дальнейшие шаги:")
    print("1. Проверьте DEBUG=False в .env файле")
    print("2. Убедитесь, что ALLOWED_HOSTS содержит ваш домен")
    print("3. Загрузите проект на хостинг")
    print("4. Настройте WSGI/ASGI сервер (gunicorn)")
    print("5. Настройте веб-сервер (nginx) при необходимости")

if __name__ == "__main__":
    main()