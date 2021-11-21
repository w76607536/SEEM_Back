from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from logistic_solution.models import Place
from logistic_solution.serializers import PlaceSerializer
from logistic_solution.GoogleMapAPI.GoogleMaps import GoogleMaps
from logistic_solution.common import *

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        #print(content)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
@api_view(['GET', 'POST'])
def startPlace_list(request):
    """
    列出所有的code snippet，或创建一个新的snippet。
    """
    if request.method == 'GET':
        startPlaces = Place.objects.filter(is_startPlace=False)
        serializer = PlaceSerializer(startPlaces, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        googleMapsTool = GoogleMaps()
        data['place_id'], data['lat'], data['lng'] = googleMapsTool.place_inquire(data["name"])
        serializer = PlaceSerializer(data=data)
        #print(data)
        if serializer.is_valid():
            serializer.create(data)
            return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def place_detail(request, pk):
    """
    获取，更新或删除一个 code snippet。
    """
    try:
        place = Place.objects.get(pk=pk)
    except Place.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlaceSerializer(place)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PlaceSerializer(place, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        place.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['POST'])
def solution_list_selectPlace(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        startPlace = Place.objects.get(id = data['placeId'])
        duration = int(data['duration'])
        resultList = solution_list_normal(startPlace,duration)
        return JSONResponse(resultList)

@csrf_exempt
@api_view(['POST'])
def solution_list_selectedPlace(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        startPlace = Place.objects.get(id = data['placeId'])
        duration = int(data['duration'])
        resultList = solution_list_normal(startPlace,duration)
        return JSONResponse(resultList)

@csrf_exempt
@api_view(['POST'])
def solution_list_inputPlace(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        name = data["name"]
        startPlace = Place()
        startPlace.name = name
        googleMapsTool = GoogleMaps()
        startPlace.place_id,startPlace.lat,startPlace.lng = googleMapsTool.place_inquire(data["name"])
        duration = int(data['duration'])
        resultList = solution_list_normal(startPlace,duration)
        return JSONResponse(resultList)
