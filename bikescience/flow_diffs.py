import pandas as pd

from . import flow
from . import tiers
from . import arrow
from . import interface as interf


def diffs_map(start_trips, end_trips, grid, stations, stations_distances, perc_below):
    start_od = flow.od_countings(start_trips, grid, stations)
    start_gs = flow.grid_and_stations
    end_od = flow.od_countings(end_trips, grid, stations)
    end_gs = flow.grid_and_stations
    merge = start_od.merge(end_od, on=['i_start', 'j_start', 'i_end', 'j_end'], how='outer') \
            [['i_start', 'j_start', 'i_end', 'j_end',          # cell identifier
              'trip counts_x', 'origin_x', 'destination_x',    # first period
              'trip counts_y', 'origin_y', 'destination_y']]   # second period
    merge = merge[(merge['i_start'] != merge['i_end']) | (merge['j_start'] != merge['j_end'])]
    
    start_tiers, _ = tiers.find_tiers(start_od, start_trips, start_gs, stations_distances, max_tiers=4)
    start_top = start_tiers.loc[0]
    start_second = start_tiers.loc[1]
    start_how_many_below = (start_top['top'] - start_top['min']) * perc_below / 100.0

    end_tiers, _ = tiers.find_tiers(end_od, end_trips, end_gs, stations_distances, max_tiers=4)
    end_top = end_tiers.loc[0]
    end_second = end_tiers.loc[1]
    end_how_many_below = (end_top['top'] - end_top['min']) * perc_below / 100.0
    
    considering = merge[(merge['trip counts_x'] >= start_second['top'] - start_how_many_below) |
                        (merge['trip counts_y'] >= end_second['top'] - end_how_many_below)]
    
    fmap = grid.map_around(zoom=13)
    weight = 1
    for idx, row in considering.iterrows():
        if (not pd.isnull(row['trip counts_x'])) and (not pd.isnull(row['trip counts_y'])):
            start_in_4th = row['trip counts_x'] >= start_second['top']
            end_in_4th = row['trip counts_y'] >= end_second['top']
            if start_in_4th or end_in_4th:
                text = '{:.0f} trips before, {:.0f} trips after'.format(row['trip counts_x'], row['trip counts_y'])
                arrow.draw_arrow(fmap,
                                 row['origin_y'].y, row['origin_y'].x, row['destination_y'].y, row['destination_y'].x,
                                 text=text, weight=weight, color='blue', radius_fac=2.0)
        elif pd.isnull(row['trip counts_y']):
            if row['trip counts_x'] >= start_second['top']:
                text = '{:.0f} old trips'.format(row['trip counts_x'])
                arrow.draw_arrow(fmap,
                                 row['origin_x'].y, row['origin_x'].x, row['destination_x'].y, row['destination_x'].x,
                                 text=text, weight=weight, color='red', radius_fac=2.0)
        else:
            if row['trip counts_y'] >= end_second['top']:
                text = '{:.0f} new trips'.format(row['trip counts_y'])
                arrow.draw_arrow(fmap,
                                 row['origin_y'].y, row['origin_y'].x, row['destination_y'].y, row['destination_y'].x,
                                 text=text, weight=weight, color='green', radius_fac=2.0)
    return fmap