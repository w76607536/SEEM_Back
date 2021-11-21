from rest_framework import serializers
from logistic_solution.models import  Place
#from logistic_solution.GoogleMapAPI.GoogleMaps import GoogleMaps


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

    def create(self,validated_data):
        return Place.objects.create(** validated_data)



