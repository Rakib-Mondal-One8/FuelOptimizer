from api.models import FuelStation
from api.services.geocoder import GeocodingService


stations = FuelStation.objects.filter(latitude__isnull=True)

for station in stations:
    address = f"{station.address}, {station.city}, {station.state}, USA"

    # print(address)
    coordinates = GeocodingService().geocode(address=address)
    # print(coordinates)

    station.latitude = coordinates['latitude']
    station.longitude = coordinates['longitude']
    station.save()


