from django.core.management.base import BaseCommand, CommandError
from entreprises.models import Entreprise, Result
import json


class Command(BaseCommand):
    help = "Delete existing data and insert initial data from raw JSON file"

    def handle(self, *args, **options):
        entreprises = Entreprise.objects.all()
        entreprises.delete()
        self.stdout.write(self.style.SUCCESS("All current data are deleted"))

        f = open("initial_data.json")
        rawdata = json.load(f)
        f.close()

        for entreprise_data in rawdata:
            results_data = entreprise_data.pop("results")
            entreprise = Entreprise.objects.create(**entreprise_data)
            for result_data in results_data:
                Result.objects.create(entreprise=entreprise, **result_data)
        self.stdout.write(self.style.SUCCESS("Initial raw data successfully added"))
