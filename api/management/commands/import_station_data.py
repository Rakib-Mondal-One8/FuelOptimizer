import csv

from django.core.management.base import BaseCommand
from api.models import FuelStation


class Command(BaseCommand):
    help = "Import fuel stations"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str)

    def handle(self, *args, **options):
        path = options["csv_file"]

        with open(path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            stations = []

            for row in reader:
                stations.append(
                    FuelStation(
                        truckstop_id=row["OPIS Truckstop ID"],
                        truckstop_name=row["Truckstop Name"],
                        address=row["Address"],
                        city=row["City"],
                        state=row["State"],
                        rack_id=row["Rack ID"],
                        retail_price=row["Retail Price"],
                    )
                )

            FuelStation.objects.bulk_create(
                stations,
                ignore_conflicts=True
            )

        self.stdout.write(self.style.SUCCESS("Fuel stations imported!"))