from api.services import station_finder,cost
from haversine import haversine,Unit

class OptimizerService():

    def optimial_halts(self,points):
        tree, stations = station_finder.StationFinder.load_tree()

        # prefix distance from start to ith route point
        prefix_route_distance = [0]
        n = len(points['coordinates'])
        for i in range(1,n):
            prev_coor = points['coordinates'][i-1]
            cur_coor = points['coordinates'][i]
            new_dist = prefix_route_distance[i-1] + haversine(
                (prev_coor[1],prev_coor[0]),
                (cur_coor[1],cur_coor[0]),
                unit=Unit.MILES
            )

            prefix_route_distance.append(new_dist)

        # finding closest route point from each stations that lies along the route
        # and also calculating their prefix
        station_closest_route = {}
        for point_idx, point in enumerate(points['coordinates']):
            lon = float(point[0])
            lat = float(point[1])

            for station_idx in tree.query_ball_point((lat,lon),r=0.18): # 0.18 ~ 20 km 
                station = stations[station_idx]

                distance = haversine(
                    (lat,lon),
                    (station.latitude,station.longitude),
                    unit=Unit.MILES
                ) + prefix_route_distance[point_idx]

                if(
                    station_idx not in station_closest_route 
                    or distance<station_closest_route[station_idx]['distance']
                ):
                    station_closest_route[station_idx] = {
                        "route_idx" : point_idx,
                        "distance" : distance,
                    }

        return cost.CostService().calculate_cost(station_closest_route,stations,prefix_route_distance,points)
        # return stations[0].retail_price
