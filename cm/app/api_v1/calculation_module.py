from osgeo import gdal
import numpy as np
import pandas as pd
import os

from ..helper import generate_output_file_tif, create_zip_shapefiles
from ..constant import CM_NAME
import time

from ..api_v1.my_calculation_module_directory.raster_api import return_nuts_codes

path2data = os.path.split(os.path.abspath(__file__))[0]
transport_data_nuts2 = os.path.join(path2data,"my_calculation_module_directory/data/transport_nuts2.csv")


def calculation(output_directory, inputs_raster_selection):
    path_nuts_id_tif = inputs_raster_selection["nuts_id_number"]
    nuts2_codes  = return_nuts_codes(path_nuts_id_tif)
    transport_data = pd.read_csv(transport_data_nuts2)
    ids = transport_data['NUTS_ID'].values
    #flag = False
    result = dict()
    result['name'] = CM_NAME
    selected_areas = ""
    for nuts2 in nuts2_codes:
        selected_areas = selected_areas + nuts2 + " and "
    # remove the last " and "
    selected_areas = selected_areas[:-5]
    rows = np.concatenate([np.argwhere(ids == item)[:,0] for item in nuts2_codes])
    if len(rows)>0:
        transport_data_selection = transport_data.iloc[rows, :].sort_values(by=['year'])
        years = np.unique(transport_data_selection.values[:, 1])
        vehicle_stock = transport_data_selection.groupby('year')['vehicle_stock'].sum().values.astype(int)
        
        result['indicator'] = [{"unit": " ", "name": "Vehicle stock in year %s" %years[0], "value": int(vehicle_stock[0])},
                          {"unit": " ", "name": "Vehicle stock in year %s" %years[-1], "value": int(vehicle_stock[-1])},
                           ]
        if len(nuts2_codes) > 1:
            result['indicator'] = result['indicator'] + [{"unit": " ", "name": "Warning: You have selected more than one NUTS 2 region. The existing data for different years in selected regions may not be similar.", "value": str(0)}]
        graphics  = [{
                    "type": "bar",
                    "xLabel": "Year",
                    "yLabel": "Vehicle Stock)",
                    "data": {
                            "labels": [str(int(x)) for x in years],
                            "datasets": [{
                                    "label": "Vehicle stock in NUTS 2 region(s) %s" %selected_areas,
                                    "backgroundColor": ["#3e95cd"]*len(vehicle_stock),
                                    "data": [str(int(y)) for y in vehicle_stock]
                                    }]
                    }
                }]
        result['graphics'] = graphics
    else:
       result['indicator'] = [{"unit": " ", "name": "No data found for your selection", "value": 0}, ]
    return result
