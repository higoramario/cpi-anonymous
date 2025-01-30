from shapely.geometry import Point
import geopandas as gpd

def stations_geodf(stations_df):
    stations_df.reset_index(inplace=True)
    geometry = stations_df.apply(lambda row: Point(row.lon, row.lat), axis=1)
    return gpd.GeoDataFrame(data=stations_df, geometry=geometry, crs={'init': 'epsg:4326'})

def merge_trips_and_stations(trips, stations):
    with_start = trips.merge(stations, left_on='start_station_name', right_on='name')
    with_start_and_end = with_start.merge(stations, left_on='end_station_name', right_on='name', 
                                          suffixes=('_start', '_end'))
    return with_start_and_end
    
def merge_trips_stations_and_distances(trips_and_stations, stations_distances):
    return trips_and_stations.merge(stations_distances, 
                                    left_on=['index_start', 'index_end'],
                                    right_on=['id_x', 'id_y'])