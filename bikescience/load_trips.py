import glob
import pandas as pd
import holidays


years = range(2011, 2020)
boston_ma = holidays.US(state='MA', years=years)
boston_holidays = [pd.Period(freq='d', year=d.year, month=d.month, day=d.day) for d in boston_ma]


def create_time_features(trips):
    """
    ** Internal use function **
    
    Preparation of the trips dataframe.
    """
    trips['per_day'] = trips['starttime'].dt.to_period('d')
    trips['hour'] = trips['starttime'].dt.hour
    trips['week_day'] = trips['starttime'].dt.weekday
    trips['weekend'] = trips['week_day'] >= 5
    trips['holiday'] = trips['per_day'].isin(boston_holidays)
    

def load_trips_file(file):
    """
    Load some specific trip file. Returns a Pandas dataframe.
    """
    trips = pd.read_csv(file, parse_dates=['starttime', 'stoptime'])
    create_time_features(trips)
    return trips


def load_trips_files(trip_files, show=False):
    df_list = []
    for f in trip_files:
        if show:
            print(f)
        df = pd.read_csv(f, parse_dates=['starttime', 'stoptime'])
        df_list.append(df)

    trips = pd.concat(df_list)
    create_time_features(trips)
    return trips


def load_all_trips(folder, show=False):
    """
    Loads and concatenates all trip files in a folder.
    Parameters:
    - folder: self-explained
    - show: show the progress of file loading
    Returns a Pandas dataframe.
    """
    trip_files = glob.glob(folder + '/*')  
    return load_trips_files(trip_files, show)
    

def morning(trips):
    """Filter the morning trips, returning a new dataframe."""
    return trips[(trips['hour'] >= 7)  & (trips['hour'] <= 9)]

def lunchtime(trips):
    """Filter the lunchtime trips, returning a new dataframe."""
    return trips[(trips['hour'] >= 11)  & (trips['hour'] <= 13)]

def afternoon(trips):
    """Filter the afternoon trips, returning a new dataframe."""
    return trips[(trips['hour'] >= 17)  & (trips['hour'] <= 19)]

def working_days(trips):
    """Filter the working days trips, returning a new dataframe."""
    return trips[~trips['weekend'] & ~trips['holiday']]

def weekend_days(trips):
    """Filter the weekends trips, returning a new dataframe."""
    return trips[trips['weekend']]

def holiday_days(trips):
    """Filter the holiday trips, returning a new dataframe."""
    return trips[trips['holiday']]

def non_working_days(trips):
    """Filter the weekend+holiday trips, returning a new dataframe."""
    return trips[trips['weekend'] | trips['holiday']]


period_functions = [lambda trips: trips, morning, lunchtime, afternoon]
day_functions = [lambda trips: trips, working_days, weekend_days, holiday_days, non_working_days]