from django.shortcuts import render
from api.models import FuelStation
from api.serializers import FuelStationSerializer,RouteRequestSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from api.services import geocoder,routing,optimizer
from openrouteservice import convert
# Create your views here.


class FuelStationView(APIView):
    def get(self,request):
        data = FuelStation.objects.all() 
        serializer = FuelStationSerializer(data,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RouteRequestSerializer(data=request.data)

        if(serializer.is_valid()):
            source = serializer.validated_data['source']
            destination = serializer.validated_data['destination']

            #coordinates of source and destination
            get_coordinate = geocoder.GeocodingService()
            source_coordinate = get_coordinate.geocode(source)
            destination_coordinate = get_coordinate.geocode(destination)

            if(source_coordinate['latitude'] is None or
                source_coordinate['longitude'] is None or
                destination_coordinate['latitude'] is None or
                destination_coordinate['longitude'] is None
            ):
                return Response({'message':'Not a valid route!'})
            
            # print(source_coordinate,destination_coordinate,"here is the issue")

            # route from source to destination
            get_route = routing.RoutingServices()
            route_info = get_route.direction(source_coordinate,destination_coordinate)

            
            points = convert.decode_polyline(route_info['routes'][0]['geometry'])
            get_optimal_halts = optimizer.OptimizerService()
            optimal_halts = get_optimal_halts.optimial_halts(points)

            if(optimal_halts == -1):
                return Response({'message':'Not enough fuel stations along the route'})
            result = {
                'route' : points['coordinates'],
                'halts' : optimal_halts[0],
                'total_cost' : optimal_halts[1]
            }
            return Response(result)

        return Response(serializer.errors,status=400)
