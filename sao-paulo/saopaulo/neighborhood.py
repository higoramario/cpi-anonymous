from .geometry import adjacent_hexagons


def up_to_level(hex_id, level=1):
    neighborhood = {hex_id}
    l = 0
    queue = [(hex_id, l)]
    while len(queue) > 0:
        hexagon, l = queue.pop()
        if l >= level: break
        adjacent = adjacent_hexagons(hexagon)
        old = queue
        queue = [(a, l+1) for a in adjacent]
        queue.extend(old)
        neighborhood.update(adjacent)
    return neighborhood


def neighborhood_values_function(socioeconomic_df, level):
    """
    Creates a function that can be applied to a DataFrame (with `apply` method) to determine socioeconomical indicators 
    for a bigger area.
    
    Args:
        socioeconomic_df: the DataFrame which the function is going to get socioeconomical data from.
    
    Returns:
        A function that can be applied to a station list DataFrame, which has an `hex_id` column. When applied, its result 
        is a tuple for each row, whose values can be extracted by 'extract_neighborhood_columns' function.
    
    Example:
       stations['neighborhood'] = stations.apply(neighborhood_values(socioeconomic), axis=1)
       extract_neighborhood_columns(stations)
    """

    def neighborhood_values(neighborhood_row):
        count = 0
        job_qty = 0
        population = 0
        education_qty = 0
        health_qty = 0
        salaries_0_2 = 0
        salaries_2_3 = 0
        salaries_3_5 = 0
        salaries_5_10 = 0
        above_10_salaries = 0
        total_loading = 0
        total_unloading = 0
        stops_len = 0
        trips_len = 0
        
        def sum_one_hexagon(socio_row):
            nonlocal count, job_qty, population, education_qty, health_qty, \
                     salaries_0_2, salaries_2_3, salaries_3_5, salaries_5_10, above_10_salaries, \
                     total_loading, total_unloading, stops_len, trips_len
            count += 1
            job_qty += socio_row['job_qty']
            population += socio_row['population']
            education_qty += socio_row['education_qty']
            health_qty = socio_row['health_qty']
            salaries_0_2 += socio_row['0_2_salaries']
            salaries_2_3 += socio_row['2_3_salaries']
            salaries_3_5 += socio_row['3_5_salaries']
            salaries_5_10 += socio_row['5_10_salaries']
            above_10_salaries += socio_row['above_10_salaries']
            total_loading += socio_row['total_loading']
            total_unloading += socio_row['total_unloading']
            stops_len += socio_row['stops_len']
            trips_len += socio_row['trips_len']
        
        this = neighborhood_row['hex_id']
        neighbors = up_to_level(this, level)
        for id in neighbors:
            if socioeconomic_df.index.contains(id):
                sum_one_hexagon(socioeconomic_df.loc[id])
        
        return (
            job_qty,
            population,
            education_qty,
            health_qty,
            salaries_0_2 / count if count != 0 else 0,
            salaries_2_3 / count if count != 0 else 0,
            salaries_3_5 / count if count != 0 else 0,
            salaries_5_10 / count if count != 0 else 0,
            above_10_salaries / count if count != 0 else 0,
            total_loading,
            total_unloading,
            stops_len,
            trips_len
        )
    
    return neighborhood_values
    

def extract_neighborhood_columns(neighborhood_df):
    """
    Extract the values obtained by `neighborhood_values` function into separate columns.
    
    Args:
        neighborhood_df: the DataFrame with a 'neighborhood' column calculated by `neighborhood_values`.
    """
    
    neighborhood_df['neighbors_job_qty'] = neighborhood_df.apply(lambda row: row['neighborhood'][0], axis=1)
    neighborhood_df['neighbors_population'] = neighborhood_df.apply(lambda row: row['neighborhood'][1], axis=1)
    neighborhood_df['neighbors_education_qty'] = neighborhood_df.apply(lambda row: row['neighborhood'][2], axis=1)
    neighborhood_df['neighbors_health_qty'] = neighborhood_df.apply(lambda row: row['neighborhood'][3], axis=1)
    neighborhood_df['neighbors_0_2_salaries'] = neighborhood_df.apply(lambda row: row['neighborhood'][4], axis=1)
    neighborhood_df['neighbors_2_3_salaries'] = neighborhood_df.apply(lambda row: row['neighborhood'][5], axis=1)
    neighborhood_df['neighbors_3_5_salaries'] = neighborhood_df.apply(lambda row: row['neighborhood'][6], axis=1)
    neighborhood_df['neighbors_5_10_salaries'] = neighborhood_df.apply(lambda row: row['neighborhood'][7], axis=1)
    neighborhood_df['neighbors_above_10_salaries'] = neighborhood_df.apply(lambda row: row['neighborhood'][8], axis=1)
    neighborhood_df['neighbors_total_loading'] = neighborhood_df.apply(lambda row: row['neighborhood'][9], axis=1)
    neighborhood_df['neighbors_total_unloading'] = neighborhood_df.apply(lambda row: row['neighborhood'][10], axis=1)
    neighborhood_df['neighbors_stops_len'] = neighborhood_df.apply(lambda row: row['neighborhood'][11], axis=1)
    neighborhood_df['neighbors_trips_len'] = neighborhood_df.apply(lambda row: row['neighborhood'][12], axis=1)
    
    neighborhood_df.drop(['neighborhood'], axis=1, inplace=True)
    

def determine_neighborhood_indicators(neighborhood_df, socioeconomic_df, level=1):
    neighborhood_df['neighborhood'] = neighborhood_df.apply(neighborhood_values_function(socioeconomic_df, level), axis=1)
    extract_neighborhood_columns(neighborhood_df)
