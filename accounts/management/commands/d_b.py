from django.core.management.base import BaseCommand, CommandError
from main.models import Datasets, Organisations


class Command(BaseCommand):
    help = 'db update'


    def handle(self, *args, **options):

        orgs = Organisations.objects.filter(is_deleted=False)

        for org in orgs:

            count = Datasets.objects.filter(organisation=org).count()
            org.dataset_count = count

            org.save()

        self.stdout.write(self.style.SUCCESS("Successfully updated"))



        