from django.db.models.signals import post_migrate
from django.dispatch import receiver
from accounts.models import Account

@receiver(post_migrate)
def create_demo_superuser(sender, **kwargs):
    if not Account.objects.filter(username='Admin06').exists():
        Account.objects.create_superuser(
            электрондық_пошта='admin06ernur@mail.ru',
            username='Admin06',
            аты_жөні='Admin06 Ernur',
            тегі='Ernur067',
            password='Ernur2025'
        )
        print("✅ Demo superuser created.")
    else:
        print("ℹ️ Demo superuser already exists.")
