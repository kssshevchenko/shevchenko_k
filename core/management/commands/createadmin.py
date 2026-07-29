from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()

        if not User.objects.filter(username="admin"):
            User.objects.create_superuser(
                username = os.getenv("ADMIN_USERNAME"),
                password = os.getenv("ADMIN_PASSWORD"),
                email = os.getenv("ADMIN_EMAIL")
            )
