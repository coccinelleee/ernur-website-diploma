#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


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

    # Только при запуске runserver — создать демо суперюзера
    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
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

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()