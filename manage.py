#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
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
        print("✅ Demo superuser created")
    else:
        print("ℹ️ Demo superuser already exists")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Инициализация и создание суперюзера
    create_demo_superuser()

    # Запуск команды Django
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()