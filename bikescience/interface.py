from ipywidgets import widgets, Layout
import pandas as pd


def period_selector(trips, index=(0, 2)):
    """
    Generates a widget for time-filtering a trip set. The widget allows to choose a start and an end month.
    Params:
       trips - a trip dataframe
       index - a (start, end) tuple of indexes for default user selection, where 0 is the first available month (July 2011).
               The default tuple corresponds to (October 2016, September 2018) period.
    """
    start = trips['starttime'].min()
    end = trips['starttime'].max()
    options = []
    current = start
    while current < end:
        options.append((current.to_period('m').strftime('%m/%Y'), current.to_period('m')))
        current += pd.DateOffset(months=1)
    return widgets.SelectionRangeSlider(options=options, index=index, layout=Layout(width='50%'), continuous_update=False, description='Trip period')


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


def grid_delta_selector(value=0.0, min=-0.1, max=0.1):
    """Creates a slider for fine-tuning the limits of a grid"""
    return widgets.FloatSlider(min=min, max=max, value=value, step=0.001, readout_format='.3f', layout=Layout(width='50%'))