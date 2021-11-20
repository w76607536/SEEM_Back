from googleplaces import GooglePlaces, types, lang
import googlemaps
import datetime

BO_API_KEY = 'AIzaSyDQ1WqrUnV7ikvKbBqqd_L-VAycYWX_E_4'
DUAN_API_KEY = 'AIzaSyDeKdpz3cNHNu83OMquOCrPpWCJSW5j5Tw'


class GoogleMaps(object):

    def __init__(self):
        self._GOOGLE_MAPS_KEY = BO_API_KEY
        self._Google_Places = GooglePlaces(self._GOOGLE_MAPS_KEY)
        self._Google_Geocod = googlemaps.Client(key=self._GOOGLE_MAPS_KEY)

    def _text_search(self, query, language=None, location=None):
        """
        根据搜索字符串,请求google API传回推荐的列表
        :param query: 搜索字符串
        :param language: 语言
        :param location: 地区筛选
        :return:
        """
        # lat_lng = {"lat": "22.5745761", "lng": "113.9393772"}
        # 经纬度附近搜索
        # text_query_result = self.self._Google_Places.text_search(query='Gong Yuan', lat_lng=lat_lng)
        # location 为人可认识的名称
        # text_query_result = self.self._Google_Places.text_search(query='Tang Lang Shan', location='shenzhen')
        # 指定语言搜索
        text_query_result = self._Google_Places.text_search(query=query, language=language, location=location)
        return text_query_result.places

    def _reverse_geocode(self, lat, lng, language=None):
        """
        根据经纬度请求google API获取坐标信息,返回信息
        :param lat: 纬度
        :param lng:经度
        :param language:语言
        :return:
        """
        # 根据经纬度获取地址信息 pincode
        list_reverse_geocode_result = self._Google_Geocod.reverse_geocode((lat, lng), language=language)
        # print json.dumps(list_reverse_geocode_result, indent=4)
        return list_reverse_geocode_result

    def _direction_inquire(self, origin, destination, departure_time, mode):
        '''
        :param origin: 起点 经纬度字典 {'lat':,'lng'}
        :param destination: 终点 {'lat':,'lng'}
        :param departure_time: 出发时间 datetime.datetime
        :param mode: 查询出行方式
        :return:
        '''
        direction_result = self._Google_Geocod.directions(origin,destination,departure_time = departure_time,mode = mode, )
        return direction_result

    def direction_inquire(self, origin, destination, departure_time, mode='driving'):
        '''
        查询路径并解析中路经过的点，以（lat,lng) 元组表示
        :param origin: 起点
        :param destination: 终点
        :param departure_time: 出发时间 list[hour,minitues,seconds]
        :param mode: 出行方式
        :return: route_info 路径起点终点经纬度 经过的每个坐标点经纬度
        '''
        origin_location = {'lat':origin.lat, 'lng':origin.lng}
        destination_location = {'lat': destination.lat, 'lng': destination.lng}
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        departure_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, departure_time[0], departure_time[1], departure_time[2])
        result = self._direction_inquire(origin_location,destination_location,departure_time,mode)
        #print(result)
        basic_info = result[0]
        basic_info= basic_info.get('legs')[0]
        route_info = {
            'startPlaceName':origin.name,
            'startPlaceName':destination.name,
            'start_location':basic_info.get('start_location'),
            'end_location': basic_info.get('end_location'),
            'distance':basic_info.get('distance').get('text'),
            'duration':basic_info.get('duration').get('text'),
            'steps':[]
        }
        for step in basic_info.get('steps'):
            step_dict = {
                'start_location':step.get('start_location'),
                'end_location': step.get('end_location'),
                'polyline':step.get('polyline')
            }
            route_info.get('steps').append(step_dict)
        return route_info


    def place_inquire(self, name, language='zh', location='香港'):
        '''
        根据名称查询 经纬度 place id
        :param name: 地点名称
        :param language: 查询语言
        :param location: 所在城市
        :return: place_id,lat,lng
        '''
        place = self._text_search(name,language,location)[0]
        return place.place_id, place.geo_location['lat'],place.geo_location['lng']

if __name__ == '__main__':
    import json

    google_maps = GoogleMaps()
    text_search_result1 = google_maps.place_inquire("新城市广场")
    text_search_result2 = google_maps.place_inquire("香港中文大学")
    print(text_search_result1)





