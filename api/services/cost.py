from math import ceil
from api.serializers import FuelStationSerializer
from haversine import haversine, Unit

class CostService:
    stations_on_route = []
    stations = []
    points = []

    def minimum_cost(self):
        INF = 1e9
        #50 gallon fuel can be filled
        fuel_tank_size = 51
        mileage = 10
        n = len(self.stations_on_route)

        dp = [[INF] * fuel_tank_size for i in range(n+1)]
        #Base dp[n][anything] = 0
        for j in range(fuel_tank_size):
            dp[n-1][j] = 0;

        for i in range(n-2,-1,-1):
            for j in range(fuel_tank_size):
                cur_station = self.stations_on_route[i]
                station_index = cur_station['station_idx']
                fill = ceil((50 - j) * self.stations[station_index].retail_price)

                res = INF
                for k in range(i+1,n): #i+1 to n-1
                    can_go1 = j* mileage
                    can_go2 = 50 * mileage
        
                    next_station = self.stations_on_route[k]

                    # mn = min(next_station['distance'], cur_station['distance'])
                    # mx = max(next_station['distance'], cur_station['distance'])
                    closest_point = self.points[cur_station['route_idx']]
                    closest_point_lat = closest_point[1]
                    closest_point_lon = closest_point[0]

                    cur_station_lat = self.stations[station_index].latitude
                    cur_station_lon = self.stations[station_index].longitude
                    extra_distance =  haversine(
                                                (closest_point_lat,closest_point_lon),
                                                (cur_station_lat,cur_station_lon),
                                                unit=Unit.MILES
                                                )
                    
                    distance = ceil(next_station['distance'] - cur_station['distance'])
                    fuel_need = ceil(distance/10)
                    # print(distance,fuel_need)
                    if(distance <= can_go1): res = min(res,dp[k][j - fuel_need])
                    if(distance<=can_go2): res = min(res,dp[k][50 - fuel_need] + fill)

                dp[i][j] = min(dp[i][j],res)

        path = []
        i = 0
        j = 50

        while(i!=n-1):
            cur_station = self.stations_on_route[i]
            retail_price = self.stations[cur_station['station_idx']].retail_price
            fill = ceil((50 - j)*retail_price)

            found = False
            for k in range(i+1,n):
                next_station = self.stations_on_route[k]
                distance = next_station['distance'] - cur_station['distance']

                fuel_need = ceil(distance/10)
                # if not fill
                if(distance <= j*mileage and dp[i][j]==dp[k][j - fuel_need]):
                    i = k
                    j = j-fuel_need
                    found = True
                    break

                # if fill
                
                if(distance<=j*mileage and dp[i][j] == dp[k][50-fuel_need]+fill):
                    i = k
                    j = 50-fuel_need

                    serializer = FuelStationSerializer(self.stations[next_station['station_idx']])
                    path.append(serializer.data)
                    found = True
                    break

            if not found:
                return -1

        return path,dp[0][50]
        # return dp[0][50]


    def calculate_cost(self,station_closest_route,stations,prefix_route_distance,points):
        self.stations = stations
        self.stations_on_route = [
            {
                'station_idx': -1,
                'route_idx': -1,
                'distance': 0,
            }
        ]
        self.points = points['coordinates']
        ordered_stations = [
        {
            "station_idx": station_idx,
            **info
        }
        for station_idx, info in sorted(
            station_closest_route.items(),
            key=lambda x: (x[1]["route_idx"],x[1]['distance'])
        )
        ]

        for station in ordered_stations:
            self.stations_on_route.append(station)

        dest = {
            'station_idx':-1,
            'route_idx':-1,
            'distance': prefix_route_distance[-1]
        }
        self.stations_on_route.append(dest)

        # self.minimum_cost(len(self.stations_on_route))
        return self.minimum_cost()
        # return self.stations_on_route





