import pandas as pd
import json
import urllib.request as req
from pandas.io.json import json_normalize
from datetime import datetime


def load_socioeconomic():
    socioeconomic = pd.read_csv('data/scipopulis/hexagons_features.csv')
    socioeconomic = socioeconomic[['hex_id', 'total_loading', 'total_unloading', 'stops_len', 'trips_len',
                                   'job_qty', 'population', 'education_qty', 'health_qty', '0_2_salaries',
                                   '2_3_salaries', '3_5_salaries', '5_10_salaries', 'above_10_salaries']]
    socioeconomic.set_index('hex_id', inplace=True)
    return socioeconomic


def load_hexagons():
    file = open('data/scipopulis/hexagons_saopaulo_sp.json')
    hexagons = json.load(file)
    return hexagons['features']


def load_bikestations(network_list):
    bikestations = []
    for network in network_list:
        file = req.urlopen('https://api.citybik.es/v2/networks/' + network).read()
        network_data = json.loads(file.decode())
        bikestations += network_data['network']['stations']
    return bikestations


def load_station_usage():
    return pd.read_csv('data/output/station_usage_metric.csv')


def load_usage_variation():
    usage_variation = pd.read_csv('data/output/usage_variation.csv', parse_dates=['per_hour'])
    return usage_variation


def load_accessibility(geographical):
    with open('data/accessibility/sao_paulo_stations_accessibility.json') as f:
        json_dict = json.load(f)
    accessibility = json_normalize(json_dict['stations'])
    
    with open('data/accessibility/SP_station_information.json') as f:
        json_dict = json.load(f)
    station_ids = json_normalize(json_dict['data']['stations'])
    
    station_accessibility = accessibility \
        .merge(station_ids, on='station_id', how='inner') \
        [['name', 'in_accessibility', 'out_accessibility']]  \
        .merge(geographical, left_on='name', right_on='station_name', how='inner') \
        [['station_id', 'name', 'in_accessibility', 'out_accessibility']]
    
    return station_accessibility


def load_weather():
    weather = pd.read_csv('data/inmet/bdmep_inmet.csv', delimiter=';', index_col=False)
    weather.drop(['Estacao'], axis=1, inplace=True)
    weather.columns = ['Date', 'Time', 'DryBulbTemperature', 'WetBulbTemperature', 'RelativeHumidity',
                       'AtmosphericPressure', 'WindDirection', 'WindSpeed', 'Cloudiness']
    return weather
    
    
def load_stations_hexagons():
    return pd.read_csv('data/output/stations_hexagons.csv')


def load_usage_weather_old():
    return pd.read_csv('data/output/usage_weather.csv', parse_dates=['per_hour'])


def parse_inmet_date_time(row):
    tstr = row['date'] + ' ' + str(row['hour'])
    return datetime.strptime(tstr, '%d/%m/%Y %H')


def load_per_hour_weather():
    weather = pd.read_csv('data/inmet/weather.csv')
    weather.columns = ['station', 'date', 'hour', 'instant_temperature', 'max_temperature', 'min_temperature',
       'instant_humidity', 'max_humidity', 'min_humidity', 'instant_dew',
       'max_dew', 'min_dew', 'atm_pressure', 'max_atm_pressure', 'min_atm_pressure', 
       'wind_direction', 'wind_velocity', ' wind_gust', 'radiation', 'precipitation']
    weather['per_hour'] = weather.apply(parse_inmet_date_time, axis=1)
    return weather
    
    
def load_unbalance_index():
    return pd.read_csv('data/output/unbalance_index.csv', parse_dates=['per_day'])
