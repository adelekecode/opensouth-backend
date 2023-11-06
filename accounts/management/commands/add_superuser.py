from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create Superuser'


    def handle(self, *args, **options):
        
        email = input("Email:\n>")
        password = input("Password:\n>")
        
        
        User.objects.create_superuser(email=email, password=password)
        
        self.stdout.write(self.style.SUCCESS("Successfully added superuser"))