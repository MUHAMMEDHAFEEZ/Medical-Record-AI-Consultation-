from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Create a default superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        try:
            superuser = User.objects.create_superuser(
                username='admin',
                email='admin@drai.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
        except IntegrityError:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
