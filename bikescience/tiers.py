import pandas as pd
from collections import OrderedDict
from . import flow

# STEP 1: separate OD flows into tiers. 
# Returns: basic tiers DF and a tiers column to be added to the OD
def separate_into_tiers(od, trips, grid_and_stations, max_tiers):
    """ ** Internal use function ** """
    flows = od['trip counts']
    total = flows.sum()

    tiers = []
    tops = []
    mins = []
    flow_counts = []
    flows_perc = []
    partial = 0
    
    num_flows = 0
    new_tier = True
    
    trip_tiers = []
    tier = max_tiers - 1
    for value in flows:
        if new_tier:
            top = value
            new_tier = False
        
        trip_tiers.append(tier+1)
        num_flows +=1
        partial += value
        
        if partial >= ((max_tiers - tier) * total / max_tiers):
            flow_counts.append(num_flows)
            flows_perc.append(100*num_flows/flows.size)
            tiers.append(tier+1)
            tops.append(top)
            mins.append(value)
            new_tier = True
            tier -= 1
            num_flows = 0
        
    return pd.DataFrame(OrderedDict([('tier', tiers), ('top', tops), ('min', mins), ('flow_counts', flow_counts), 
                                     ('flows_perc', flows_perc)])), \
           trip_tiers

# STEP 2: merge OD (with tiers added) with trip data
# Returns: for each trip, its tier, trip duration and distance
def merge_od_and_trips(trips, stations_distances, grid_and_stations, od):
    """ ** Internal use function ** """
    trips_merges = trips \
        .merge(stations_distances, left_on=['start station id', 'end station id'], 
               right_index=True, how='left') \
         [['start station id', 'end station id', 'tripduration', 'distance']] \
        .merge(grid_and_stations, left_on='start station id', right_on='station id') \
        .merge(grid_and_stations, left_on='end station id', right_on='station id') \
         [['tripduration', 'distance', 'i_x', 'j_x', 'i_y', 'j_y']]
    trips_merges.columns = ['tripduration', 'distance', 'i_start', 'j_start', 'i_end', 'j_end']
    return trips_merges \
           .merge(od, on=['i_start', 'j_start', 'i_end', 'j_end']) \
            [['tripduration', 'distance', 'tier']]

# STEP 3: calculate medians
def aggregate_per_tier(trips_merges):
    """ ** Internal use function ** """
    agg = trips_merges.groupby('tier', as_index=False) \
                      .agg(OrderedDict([('tripduration', ['median', 'mean']), 
                                        ('distance', ['median', 'mean', 'count'])]))
    agg.columns = ['tier', 'median_duration', 'mean_duration', 'median_distance', 'mean_distance', 'trip_count']
    return agg

# STEP 4: count short and long trips for each tier
def short_and_long_trips(trips_merges):
    """ ** Internal use function ** """
    short_trips = trips_merges[trips_merges['distance'] < 1.5].groupby('tier', as_index=False).agg({'distance': 'count'})
    short_trips.columns = ['tier', 'short_count']
    long_trips = trips_merges[trips_merges['distance'] > 4.0].groupby('tier', as_index=False).agg({'distance': 'count'})
    long_trips.columns = ['tier', 'long_count']
    return short_trips, long_trips

# STEP 5: merge tiers, medians, short and long trip counts
def merge_tiers_and_trips(tiers_df, per_tier_agg, short_trips, long_trips):
    """ ** Internal use function ** """
    all_merges = tiers_df.merge(per_tier_agg, on='tier') \
                         .merge(short_trips, on='tier', how='left') \
                         .merge(long_trips, on='tier', how='left')
    all_merges['short_count_perc'] = all_merges['short_count'] / all_merges['trip_count'] * 100.0
    all_merges['long_count_perc'] = all_merges['long_count'] / all_merges['trip_count'] * 100.0
    return all_merges

# API FUNCTIONS
def find_tiers(od, trips, grid_and_stations, stations_distances, max_tiers):
    """
    Separate OD flows into tiers, each one containing 1/max_tiers of the trips, so that the 1st tier
    has the flows with most few trips, and the last tier has the flows with most trips.
    
    Parameters:
      od - an Origin-Destination counting calculated by flow.od_countings(...)
      trips - basic trip data
      grid_and_stations - after flow_od.countings(...) call, this dataframe is cached in the flows.grid_and_stations variable,
                          and can be reused (see find_tiers_raw function below for an example)
      stations_distances - the distances file loaded with stations.distances(...)
      max_tiers - the number of quantiles which the trips are divided into
      
    Returns a tuple with:
    - the tiers dataframe
    - the association between trips and tiers, with some variables for distribution plotting (e.g. the violinplots in the paper)
    """
    od.sort_values('trip counts', ascending=False, inplace=True)
    tiers_df, trip_tiers = separate_into_tiers(od, trips, grid_and_stations, max_tiers)
    
    od['tier'] = trip_tiers
    trips_merges = merge_od_and_trips(trips, stations_distances, grid_and_stations, od)
    
    per_tier_agg = aggregate_per_tier(trips_merges)
    short_trips, long_trips = short_and_long_trips(trips_merges)
    
    all_merges = merge_tiers_and_trips(tiers_df, per_tier_agg, short_trips, long_trips)
    return all_merges, trips_merges


def find_tiers_raw(trips, grid, stations, stations_distances, max_tiers=4):
    """
    Convenience function for tiers determination when there are no previously calculated OD.
    It is an example on how to do it from scratch!
    
    Parameters:
      trips - the trips dataframe
      grid - the grid object
      stations - the stations dataframe
      stations_distances - previously calculated distances between stations
      max_tiers - number of tiers to divide the trips into
      
    Returns the same as find_tiers.
    """
    od = flow.od_countings_simple(trips, grid, stations)
    tiers, trips_merges = find_tiers(od, trips, flow.grid_and_stations, stations_distances, max_tiers)
    tiers = tiers[['tier', 'min', 'top', 'flow_counts', 'flows_perc', 'median_distance', 'median_duration', 
                   'short_count_perc', 'long_count_perc']]
    tiers.columns = ['tier', 'min trips', 'max trips', '# flows', '%flows', 'median distance', 'median duration', '% short trips', 
                     '% long trips']
    return tiers, trips_merges
