from dateutil import parser
from datetime import timedelta


delta = timedelta(days=1)


def nearest_measure_date(row):
    dt = row['per_hour']

    twenty_one = dt.replace(hour=21, minute=0, second=0, microsecond=0) 
    tomorrow = dt.replace(hour=0, minute=0, second=0, microsecond=0) + delta
    
    if dt < twenty_one: return dt.strftime('%d/%m/%Y')
    return tomorrow.strftime('%d/%m/%Y')


def nearest_measure_time(row):
    dt = row['per_hour']
    
    six = dt.replace(hour=6, minute=0, second=0, microsecond=0)
    fifteen = dt.replace(hour=15, minute=0, second=0, microsecond=0)
    twenty_one = dt.replace(hour=21, minute=0, second=0, microsecond=0) 
    tomorrow = dt.replace(hour=0, minute=0, second=0, microsecond=0) + delta
    
    if dt < six: return 0
    if dt < fifteen: return 1200
    if dt < twenty_one: return 1800
    return 0
    
    
def determine_nearest_measure_times(df):
    print('Extracting an INMET-like Date column...')
    df['Date'] = df.apply(nearest_measure_date, axis=1)
    print('Extracting an INMET-like Time column...')
    df['Time'] = df.apply(nearest_measure_time, axis=1)
    pass
