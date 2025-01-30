import json
from h3 import h3
import math
from shapely.geometry import Polygon
import geopandas as gpd
import folium

from .tiers import separate_into_tiers
from .arrow import draw_arrow


def extract_flows_and_tiers(trips, zoom=9):

    def encode_od_points(row):
        start_lat = row['start station latitude']
        start_lon = row['start station longitude']
        end_lat = row['end station latitude']
        end_lon = row['end station longitude']
        return h3.geo_to_h3(start_lat, start_lon, zoom), \
               h3.geo_to_h3(end_lat, end_lon, zoom), \
               start_lat, start_lon, end_lat, end_lon

    trips[['start_hash', 'end_hash', 'start_lat', 'start_lon', 'end_lat', 'end_lon']] = \
            trips.apply(encode_od_points, axis=1, result_type='expand')
    od_counts = trips.groupby(['start_hash', 'end_hash'], as_index=False) \
                      .agg({'tripduration': 'count',
                            'start_lat': 'mean', 'start_lon': 'mean',
                            'end_lat': 'mean', 'end_lon': 'mean'})
    od_counts.rename(columns={'tripduration': 'trip counts'}, inplace=True)
    od_counts.sort_values('trip counts', ascending=False, inplace=True)
    tiers4, _ = separate_into_tiers(od_counts, None, None, max_tiers=4)
    return od_counts, tiers4


def plot_hexagons(fmap, lat, lon, zoom, n_rings, style=lambda x: {'color': 'black', 'weight': 0.5, 'opacity': 0.3, 'fillOpacity': 0.0}):
    hex_ids = []
    geometries = []
    h3_key = h3.geo_to_h3(lat, lon, zoom)
    rings = h3.k_ring_distances(h3_key, n_rings)

    for r in rings:
        for h in r:
            xy_boundaries = []
            lat_long_boundaries = h3.h3_to_geo_boundary(h)
            for b in lat_long_boundaries:
                xy_boundaries.append([b[1], b[0]])
            hex_ids.append(h)
            geometries.append(Polygon(xy_boundaries))

    geodf = gpd.GeoDataFrame(data={'hex_id': hex_ids, 'geometry': geometries}, crs={'init': 'epsg:4326'})
    folium.GeoJson(geodf.to_json(), style_function=style).add_to(fmap)
    

POPUP_NUM_TRIPS = 0
POPUP_FLOW_ID = 1

def flow_map(fmap, od_df, minimum=-1, maximum=-1, show=4, radius=1.0, text=POPUP_NUM_TRIPS):

    # eliminate round-trips to the same station, which are not considering in this analysis
    filtered = od_df[od_df.start_hash != od_df.end_hash]

    if maximum == -1:
        maximum = filtered['trip counts'].max()
    if minimum == -1:
        minimum = maximum / show
        
    total_trips = filtered['trip counts'].sum()

    filtered = filtered[((filtered['trip counts'] >= minimum) & (filtered['trip counts'] <= maximum))]

    shown_trips = 0
    
    for idx, row in filtered.iterrows():
        num_trips = row['trip counts']
        
        shown_trips += num_trips
        weight = math.ceil( (num_trips-minimum)/maximum * 10)
        if weight == 0: weight = 1
        
        if text == POPUP_NUM_TRIPS:
            text_plot = str(num_trips) + ' bike trips'
        else:
            text_plot = 'Start: ' + row['start_hash'] + ' / End: ' + row['end_hash']

        try:
            draw_arrow(fmap, row.start_lat, row.start_lon, row.end_lat, row.end_lon, 
                   text=text_plot,
                   weight=weight,
                   radius_fac=radius)
        except Exception as e:
            print(row)
            raise e
