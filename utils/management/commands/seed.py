import email
from api.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate database with testing data."

    def handle(self, *args, **options):
        try:
            user = User.objects.create_user(
                id="ea0212d3-abd6-406f-8c67-868e814a2436",
                first_name="first",
                last_name="last",
                username="username",
                email="user@miniwallet.id",
                password="password",
                is_staff=False,
                is_active=True
            )
            print(f"User already created with username: {user.username} and email: {user.email}")
        except Exception as e:
            print(e)