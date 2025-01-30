import geopandas as gpd
import pandas as pd

from . import grid

H_DISPLACEMENT = 0.004
V_DISPLACEMENT = 0.003

#default grid size = 20
placement1 = grid.Grid().geodataframe()
placement2 = grid.Grid(west_limit=grid.default_west_limit - H_DISPLACEMENT, 
                       east_limit=grid.default_east_limit - H_DISPLACEMENT, 
                       north_limit=grid.default_north_limit + V_DISPLACEMENT, 
                       south_limit=grid.default_south_limit + V_DISPLACEMENT).geodataframe()

placement1_10 = grid.Grid(n=10).geodataframe()
placement2_10 = grid.Grid(n=10,
                          west_limit=grid.default_west_limit - H_DISPLACEMENT, 
                          east_limit=grid.default_east_limit - H_DISPLACEMENT, 
                          north_limit=grid.default_north_limit + V_DISPLACEMENT, 
                          south_limit=grid.default_south_limit + V_DISPLACEMENT).geodataframe()

placement1_30 = grid.Grid(n=30).geodataframe()
placement2_30 = grid.Grid(n=30,
                          west_limit=grid.default_west_limit - H_DISPLACEMENT, 
                          east_limit=grid.default_east_limit - H_DISPLACEMENT, 
                          north_limit=grid.default_north_limit + V_DISPLACEMENT, 
                          south_limit=grid.default_south_limit + V_DISPLACEMENT).geodataframe()

placement1_40 = grid.Grid(n=40).geodataframe()
placement2_40 = grid.Grid(n=40,
                          west_limit=grid.default_west_limit - H_DISPLACEMENT, 
                          east_limit=grid.default_east_limit - H_DISPLACEMENT, 
                          north_limit=grid.default_north_limit + V_DISPLACEMENT, 
                          south_limit=grid.default_south_limit + V_DISPLACEMENT).geodataframe()