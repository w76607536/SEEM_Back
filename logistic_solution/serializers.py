from rest_framework import serializers
from logistic_solution.models import  Place,Path
from logistic_solution.GoogleMapAPI.GoogleMaps import GoogleMaps


class PlaceSerializer(serializers.Serializer):

    class Meta:
        model = Place
        fields = ('id', 'name', 'place_id', 'lat', 'lng', 'score', 'is_startPlace')

    def create(self,validated_data):
        return Place.objects.create(** validated_data)



