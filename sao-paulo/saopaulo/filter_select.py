from datetime import date

holiday_dates = [
    date(2018, 5, 31),
    date(2018, 7, 9),
    date(2018, 9, 7),
    date(2018, 10, 12),
    date(2018, 10, 15),
    date(2018, 10, 28),
    date(2018, 11, 2),
    date(2018, 11, 15),
    date(2018, 11, 20),
    date(2018, 12, 25),
]

days_of_week = [('Mon', 0), ('Tue', 1), ('Wed', 2), ('Thu', 3), ('Fri', 4), ('Sat', 5), ('Sun', 6)]

def station_from_citybikes_array(array):
    key_values = []
    for i in range(len(array)):
        key_values.append((array[i]['name'], i))
    return key_values
    
def station_from_dataframe(df, name_field='name', id_field='id'):
    return zip(df[name_field].tolist(), df[id_field].tolist())

def filter_weekend_and_holidays(df, include):
    weekend = df['per_hour'].dt.dayofweek.isin([5, 6])
    holidays = df['per_hour'].dt.date.isin(holiday_dates)
    if include:
        return df[weekend | holidays]
    else:
        return df[~weekend & ~holidays]
