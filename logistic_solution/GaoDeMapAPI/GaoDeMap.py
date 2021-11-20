import requests

URL_Location = 'https://restapi.amap.com/v3/geocode/geo?address='
URL_Parameter_city = '&city='
URL_Parameter_output = '&output='
URL_Parameter_key = '&key='
CITYCODE = '1852'
ADCODE = '810000'

class GaoDeMaps(object):

    def __init__(self, output = 'JSON', city = CITYCODE):
        self._GAODE_MAPS_KEY = '50080b034a44aedc5fe9a6e02901650f'
        self._Parameter = URL_Parameter_city + city + URL_Parameter_output + output + URL_Parameter_key + self._GAODE_MAPS_KEY

    def inquireLocation(self, address):
        url = URL_Location + address + self._Parameter
        response = requests.request("GET", url)
        #print(response.text)


if __name__ =='__main__':
    gaodeMaps = GaoDeMaps()
    location_result = gaodeMaps.inquireLocation('新城市广场')




