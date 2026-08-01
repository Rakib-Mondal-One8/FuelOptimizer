import requests
from django.conf import settings

class RoutingServices:
    BASE_URL = 'https://api.openrouteservice.org/v2/directions/driving-car'

    def direction(self,source,destination):
        headers = {
            'Authorization' : settings.ORS_API_KEY,
            'Content-Type' : 'application/json'
        }

        body = {
            'coordinates' : [
                [source['longitude'],source['latitude']],
                [destination['longitude'],destination['latitude']]
            ],
            'geometry' : True
        }

        response = requests.post(
            self.BASE_URL,
            headers=headers,
            json=body,
            timeout=10
        )
        # print(response.status_code)
        # print(response.text)
        response.raise_for_status()

        data = response.json()

        return data


        