from ipywidgets import widgets, Layout
import pandas as pd
import numpy as np
#import tembici.stations as st

def period_selector(trips, index=(0, 1)):
    """
    Generates a widget for time-filtering a trip set. The widget allows to choose a start and an end month.
    Params:
       trips - a trip dataframe
       index - a (start, end) tuple of indexes for default user selection, where 0 is the first available month (July 2011).
               The default tuple corresponds to (October 2016, September 2018) period.
    """
    start = trips['starttime'].min()
    end = trips['starttime'].max()
    options = [(i.to_period('m').strftime('%m/%Y'), i.to_period('m')) for i in pd.date_range(start, end, freq='m')]
    index = len(options)-1
    return widgets.SelectionRangeSlider(options=options, index=(0,index), continuous_update=False)


def period_interval(selected_period):
    """
    Determines Pandas timestamps corresponding to a period selected by the user.
    Returns the (start, end) tuple of timestamps, which can be used for filtering like so:
    
       df[(df.my_timestamp >= start) & (df.my_timestamp < end)]
       
    - 'start' is the 1st day of the first month
    - 'end' is the 1st day of the month after the last
    thus embracing all days over the selected period.
    """
    start = selected_period[0].to_timestamp()
    end = selected_period[1].to_timestamp() + pd.DateOffset(months=1)
    return start, end


def grid_delta_selector(value=0.0, min=-0.1, max=0.1,label=''):
    """Creates a slider for fine-tuning the limits of a grid"""
    return widgets.FloatSlider(min=min, max=max, value=value, step=0.001, readout_format='.3f',description=label)


def age_selector():
    """
    Generates a widget for age range. The widget allows to choose a start and an end age.
    """
    return widgets.SelectionRangeSlider(options=range(10,91), index=(0,len(range(10,91))-1), continuous_update=False)

#def distance_selector(trips,stations,stations_distances):
#    """
#    Generates a widget to filter trips per distance. 
#    Params:
#       trips - a trip dataframe
#       stations_distances - a dataframe with stations
#       stations_distances - a dataframe with distances among stations
#    """
#    trips = st.merge_trips_and_stations(trips, stations)
#    trips = st.merge_trips_stations_and_distances(trips, stations_distances)
#
#    distance_max = int(np.ceil(trips['distance'].max()))
#            
#    return widgets.SelectionRangeSlider(options=range(0,distance_max), index=(0,len(range(0,distance_max))-1), continuous_update=False)


def duration_selector(trips):
    """
    Generates a widget to filter trips per duration. 
    Params:
       trips - a trip dataframe
    """
    expected_max = 60
    duration_min = int(trips['tripduration'].min()/60)
    if duration_min < 1:
        duration_min = 1
    duration_max = int(np.ceil(trips['tripduration'].max()/60))
    range_max = range(duration_min,duration_max)
    index_max = len(range_max)-1
    if expected_max in range_max:
        index_max = range_max.index(expected_max)
    if duration_max > 90:
        duration_max = 90
    
    return widgets.SelectionRangeSlider(options=range(duration_min,duration_max+1), index=(0,index_max), continuous_update=False)
    
def duration_selector_min(trips):
    """
    Generates a widget to filter trips per duration. 
    Params:
       trips - a trip dataframe
    """
    duration_min = int(trips['tripduration'].min()/60)
    if duration_min < 1:
        duration_min = 1
    
    duration_max = int(np.ceil(trips['tripduration'].max()/60))
    
    return widgets.IntText(value=duration_min, min=duration_min, max=duration_max, continuous_update=False)

def duration_selector_max(trips):
    """
    Generates a widget to filter trips per duration. 
    Params:
       trips - a trip dataframe
    """
    duration_min = int(trips['tripduration'].min()/60)
    if duration_min < 1:
        duration_min = 1
    
    duration_max = int(np.ceil(trips['tripduration'].max()/60))
    
    return widgets.IntText(value=duration_max, min=duration_min, max=duration_max, continuous_update=False)

def duration_selector_box(trips):
    """
    Generates a widget to filter trips per duration. 
    Params:
       trips - a trip dataframe
    """
    duration_min = int(trips['tripduration'].min()/60)
    if duration_min < 1:
        duration_min = 1
    min_widget = widgets.IntText(value=duration_min, continuous_update=False)
    
    duration_max = int(np.ceil(trips['tripduration'].max()/60))
    max_widget = widgets.IntText(value=duration_max, continuous_update=False)
    
    return widgets.HBox([min_widget,max_widget])
