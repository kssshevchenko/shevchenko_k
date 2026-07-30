from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv("ADMIN_USERNAME")
        password = os.getenv("ADMIN_PASSWORD")
        email = os.getenv("ADMIN_EMAIL")

        user, created = User.objects.get_or_create(username=username)
        user.email = email
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
