from .filter_select import filter_weekend_and_holidays

    
def compute_usage_variation(history, period_field):
    
    def compute_usage_variation_function(col):
        inc = 0
        dec = 0
        ant = None
        for val in col:
            if ant:
                if val > ant:
                    inc += val - ant
                elif val < ant:
                    dec += ant - val
            ant = val
        return (inc, dec)
    
    grouping = history.groupby(['id', 'name', period_field], as_index=False)
    usage_variation = grouping.agg({'free_bikes': compute_usage_variation_function})
    usage_variation['free_bikes_increase'] = usage_variation.apply(lambda row: row['free_bikes'][0], axis=1)
    usage_variation['free_bikes_decrease'] = usage_variation.apply(lambda row: row['free_bikes'][1], axis=1)
    usage_variation = usage_variation.drop(['free_bikes'], axis=1)
    return usage_variation


def calculate_usage_metric(df):

    def calculate_usage_metric_function(col):
        with_variation = 0
        without_variation = 0
        for val in col:
            if val == 0:
                without_variation += 1
            else:
                with_variation += val
        return with_variation / without_variation if without_variation != 0 else with_variation

    weekend_and_holidays = filter_weekend_and_holidays(df, include=True) 
    work_days = filter_weekend_and_holidays(df, include=False)
    
    general = df.groupby(['id', 'name', df['per_hour'].dt.to_period('d').dt.to_timestamp()], as_index=False) \
                     .agg({'free_bikes_increase': 'sum'}) \
                     .groupby(['id', 'name'], as_index=False).agg({'free_bikes_increase': 'mean'})
    
    weekend_and_holidays = weekend_and_holidays \
                    .groupby(['id', 'name', weekend_and_holidays['per_hour'].dt.to_period('d').dt.to_timestamp()], as_index=False) \
                    .agg({'free_bikes_increase': 'sum'}) \
                    .groupby(['id', 'name'], as_index=False) \
                    .agg({'free_bikes_increase': 'mean'})
    
    work_days = work_days \
                    .groupby(['id', 'name', work_days['per_hour'].dt.to_period('d').dt.to_timestamp()], as_index=False) \
                    .agg({'free_bikes_increase': 'sum'}) \
                    .groupby(['id', 'name'], as_index=False) \
                    .agg({'free_bikes_increase': 'mean'})
    
    station_usage = general \
            .merge(weekend_and_holidays, on=['id', 'name'], how='left') \
            .merge(work_days, on=['id', 'name'], how='left')
    station_usage.columns = ['id', 'name', 'general_daily_increase', 'weekend_and_holidays_daily_increase', 'work_days_daily_increase']
    return station_usage
    
    
def calculate_balance_index_function(exponent):
    def calculate_balance_index(row):
        capacity = row['free_bikes'] + row['empty_slots']
        half = capacity / 2
        unbalance_index = (row['free_bikes'] - half) / half
        return unbalance_index**exponent
    return calculate_balance_index
    
    
    
