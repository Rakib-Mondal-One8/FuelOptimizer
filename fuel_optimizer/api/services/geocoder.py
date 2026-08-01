import requests
from django.conf import settings

class GeocodingService:

    BASE_URL = "https://api.geoapify.com/v1/geocode/search"
    # "https://api.openrouteservice.org/geocode/search"
    API_KEY = '63d31a24494642dfb7aa0b1c9ef62f9b'

    def geocode(self, address):
        headers = {
            "Authorization": self.API_KEY,
            'Content-Type' : "application/json"
        }

        params = {
            "text": address,
            "size": 1
        }

        response = requests.get(
            self.BASE_URL,
            headers=headers,
            params=params,
            timeout=50
        )

        # print(response.status_code)
        # print(response.text)
        response.raise_for_status()

        data = response.json()

        if not data["features"]:
            return {
                        "longitude": None,
                        "latitude": None
                    }
        # if not data:
        #     raise ValueError("Location not found.")

        coordinates = data["features"][0]["geometry"]["coordinates"]

        return {
            "longitude": coordinates[0],
            "latitude": coordinates[1]
        }
        # return {
        #     "latitude": float(data[0]["lat"]),
        #     "longitude": float(data[0]["lon"])
        # }