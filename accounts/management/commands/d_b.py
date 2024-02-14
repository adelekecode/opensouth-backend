from django.core.management.base import BaseCommand, CommandError
from main.models import Datasets, DatasetViews


class Command(BaseCommand):
    help = 'db update'


    def handle(self, *args, **options):

        datasets = Datasets.objects.all()
        views = DatasetViews.objects.all()

        for view in views:
            dataset = Datasets.objects.get(pk=view.dataset.pk)
            dataset.views = view.count
            dataset.save()
            
            

        
        self.stdout.write(self.style.SUCCESS("Successfully updated"))



        