#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from accounts.models import Account
from django.core.management import call_command


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
    execute_from_command_line(sys.argv)


def create_demo_superuser():
    if not Account.objects.filter(username='Admin06').exists():
        Account.objects.create_superuser(
            электрондық_пошта='admin06ernur@mail.ru',
            username='Admin06',
            аты_жөні='Admin06 Ernur',
            тегі='Ernur067',
            password='Ernur2025'
        )

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
    import django
    django.setup()
    create_demo_superuser()
    main()