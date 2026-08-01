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
                lat = row["latitude"].strip()
                lon = row["longitude"].strip()
                stations.append(
                    FuelStation(
                        truckstop_id=row["truckstop_id"],
                        truckstop_name=row["truckstop_name"],
                        address=row["address"],
                        city=row["city"],
                        state=row["state"],
                        rack_id=row["rack_id"],
                        retail_price=row["retail_price"],
                        latitude=float(lat) if lat else None,
                        longitude=float(lon) if lon else None,
                    )
                )

            FuelStation.objects.bulk_create(
                stations,
                ignore_conflicts=True
            )

        self.stdout.write(self.style.SUCCESS("Fuel stations imported!"))