#!/usr/bin/env python
"""Утилита командной строки Django для административных задач."""
import os
import sys

def create_demo_superuser():
    import django
    django.setup()
    from accounts.models import Account
    if not Account.objects.filter(username='Admin06').exists():
        Account.objects.create_superuser(
            электрондық_пошта='admin06ernur@mail.ru',
            username='Admin06',
            аты_жөні='Admin06 Ernur',
            тегі='Ernur067',
            password='Ernur2025'
        )

def main():
    """Выполнение административных задач."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что он установлен и "
            "доступен в переменной окружения PYTHONPATH. Вы забыли активировать виртуальное окружение?"
        ) from exc

    execute_from_command_line(sys.argv)

    # Создание суперпользователя после применения миграций
    if len(sys.argv) > 1 and sys.argv[1] == 'migrate':
        create_demo_superuser()

if __name__ == '__main__':
    main()
