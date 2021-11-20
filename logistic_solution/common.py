from logistic_solution.models import Path,Place
from logistic_solution.GoogleMapAPI.GoogleMaps import GoogleMaps
from django.db.models import Q
import copy

import logging

logger = logging.getLogger('log')

def initPath(if_all_init=False):
    placeList = Place.objects.all()
    for startPlace in placeList:
        for endPlace in placeList:
            if startPlace == endPlace:
                continue
            else:
                path = Path.objects.filter(startPlace__id=startPlace.id,endPlace__id=endPlace.id)
                if path and if_all_init == False :
                    logger.info('path 已存在！ startPlace:{}；endPlace:{}；'.format(startPlace.name,endPlace.name))
                    continue
                else:
                    print('查询path ！ startPlace:{}；endPlace:{}；'.format(startPlace.name, endPlace.name))
                    path = Path()
                    path.startPlace = startPlace
                    path.endPlace = endPlace
                    path_info = GoogleMaps().direction_inquire(startPlace,endPlace,[9,0,0])
                    path.distance = path_info['distance']
                    path.duration = path_info['duration']
                    path.save()
                    logger.info('添加path！ startPlace:{}；endPlace:{}；distance{};duration{}'.format(startPlace.name, endPlace.name,path.duration,path.distance))

def make_solution_normal(startPlace,maxDuration):
    solutionList =[]
    pathList = Path.objects.all()

    durationDict ={}
    for path in pathList:
        dictStr = path.startPlace.name + '--' + path.endPlace.name
        durationDict[dictStr] = float(path.duration[0:-5])
    #print(durationDict)
    solutionDict ={
        'startPlace':startPlace,
        'endPlace':None,
        'duration':0,
        'score':0,
        'pathList':[],
    }
    placeList = Place.objects.filter(~Q(id= startPlace.id))
    next_place(list(placeList),solutionList,durationDict,solutionDict,startPlace,maxDuration)
    return solutionList

def next_place(placeList,solutionList,durationDict, solutionDict, lastPlace, maxDuration ):
    #_placeList = copy.deepcopy(placeList)
    _solutionDict = copy.deepcopy(solutionDict)
    i = 0
    while True:
        if i >= len(placeList) or len(placeList) == 0:
            break
        #print(i,len(placeList))
        place = placeList[i]
        dictStr = lastPlace.name + '--' + place.name
        duration = durationDict[dictStr]
        _solutionDict['duration'] += duration
        _solutionDict['score'] += place.score
        pathDict = {
            'pointPlace' : place,
            'path' :dictStr
        }
        _solutionDict['pathList'].append(pathDict)
        _solutionDict['endPlace'] = place
        if _solutionDict['duration'] >= maxDuration:
            solutionList.append(solutionDict)
        else:
            _placeList = None
            _placeList = copy.deepcopy(placeList)
            del _placeList[i]
            if _placeList == []:
                solutionList.append(_solutionDict)
            else:
                next_place(_placeList,solutionList,durationDict, _solutionDict, place, maxDuration)
        i = i + 1

def real_time_Solution(solutionList):
    solutionResultList =[]
    for solution in solutionList:
        solutionResultDict = {
            'startPlace':{
                'name': solution['startPlace'].name,
                'score':solution['startPlace'].score,
                'lat':solution['startPlace'].lat,
                'lng':solution['startPlace'].lng,
            },
            'endPlace': {
                'name': solution['endPlace'].name,
                'score': solution['endPlace'].score,
                'lat': solution['endPlace'].lat,
                'lng': solution['endPlace'].lng,
            },
            'score':solution['score'],
            'distance':0,
            'duration':0,
            'paths':[]
        }
        startPlace = solution['startPlace']
        for path in solution['pathList']:
            endPlace = path['pointPlace']
            path_info = GoogleMaps().direction_inquire(startPlace,endPlace, [9,0,0])
            pathDict = {
                'startPlaceName':startPlace.name,
                'endPlaceName':endPlace.name,
                'path-info':path_info
            }
            solutionResultDict['paths'].append(pathDict)
            solutionResultDict['duration'] += float(path_info['duration'][0:-5])
            solutionResultDict['distance'] += float(path_info['distance'][0:-3])
            startPlace = endPlace
        solutionResultList.append(solutionResultDict)

    return solutionResultList



def main():
    startPlace = Place.objects.get(name="香港中文大学")
    solutionList = make_solution_normal(startPlace,480)
    realSolutionList = real_time_Solution(solutionList)
    print(realSolutionList,len(realSolutionList))




