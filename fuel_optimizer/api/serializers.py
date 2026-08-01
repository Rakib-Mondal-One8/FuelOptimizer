from rest_framework import serializers
from api.models import FuelStation


class FuelStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelStation
        fields = '__all__'


class RouteRequestSerializer(serializers.Serializer):
    source = serializers.CharField();
    destination = serializers.CharField();
