from django.core.management.base import BaseCommand, CommandError
from main.models import Datasets


class Command(BaseCommand):
    help = 'Create Superuser'


    def handle(self, *args, **options):

        datasets = Datasets.objects.all()
        list = []
        for dataset in datasets:
            data = {
                'type': dataset.type,
                'status': True if dataset.organisation else False

            }
            list.append(data)

        print(list)

        
            # if dataset.organisation:
            #     dataset.type = 'organisation'
            #     dataset.save()
            # else:
            #     dataset.type = 'individual'
            #     dataset.save()
           


        
        self.stdout.write(self.style.SUCCESS("Successfully deleted users"))



        