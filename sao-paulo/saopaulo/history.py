import pandas as pd

HISTORY_FILE = 'data/input/bk_stations_sp_2018-08-18.csv'

def delete_dawn(history):
    return history[history['timestamp'].dt.hour.isin([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])]

def load_history(per_day=False, per_hour=False, hour_of_day=False, day_of_week=False, include_dawn=True):
    """
    Loads the history of bike stations collected from CityBikes.
    
    Args:
        file (str): history .csv file exported from MongoDB
        per_day (bool): Creates a timestamp column for grouping by date.
        per_hour (bool): Creates a timestamp column for grouping by hour.
        hour_of_day (bool): Creates an int column for grouping by hour of day (0-23), independently of the date.
        day_of_week (bool): Creates an int column for grouping by day of week (0-6 = Sun-Sat), independently of the date.
        
        All args default to False.
        
    Returns:
        A pandas.DataFrame.
    """
    def parse_timestamp(timestamp):
        return pd.to_datetime(timestamp).tz_localize('UTC').tz_convert('America/Sao_Paulo')

    history = pd.read_csv(HISTORY_FILE, parse_dates=['timestamp'], date_parser=parse_timestamp) \
              [['id', 'name', 'timestamp', 'free_bikes', 'empty_slots']]
    history = history[(history['free_bikes'] != 0) | (history['empty_slots'] != 0)]
    
    if not include_dawn:
        history = delete_dawn(history)
    
    history['total_slots'] = history['empty_slots'] + history['free_bikes']
    history.sort_values('timestamp', inplace=True)
    
    if per_day:
        history['per_day'] = history['timestamp'].dt.to_period('d').dt.to_timestamp()
    if per_hour:
        history['per_hour'] = history['timestamp'].dt.to_period('h').dt.to_timestamp()
    if hour_of_day:
        history['hour_of_day'] = history['timestamp'].dt.hour
    if day_of_week:
        history['day_of_week'] = history['timestamp'].dt.dayofweek
        
    return history
    
    
def week_intervals(history):
    start = history['timestamp'].min().replace(hour=0, minute=0, second=0, microsecond=0)
    end = history['timestamp'].max().replace(hour=0, minute=0, second=0, microsecond=0)

    print('Start:', start.day_name(), start)
    print('End:', end.day_name(), end)

    delta = pd.Timedelta(days=1)
    next_week = end + pd.Timedelta(days=7)
    weeks = []
    week_start = start
    day = start + delta
    while day <= next_week:
        if day.day_name() == 'Sunday':
            week_filter_range = (week_start, day)  # inclusive, exclusive
            weeks.append(week_filter_range)
            week_start = day
        day += delta

    return weeks
