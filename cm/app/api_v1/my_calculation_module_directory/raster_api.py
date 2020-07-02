import os,sys
from osgeo import gdal
import numpy as np
import pandas as pd



path2data = os.path.split(os.path.abspath(__file__))[0]
path_nuts_code = os.path.join(path2data,"data/data_nuts_id_number.csv")

def get_nuts(nuts_code):
    #nuts3 = nuts_code[:5]
    nuts2 = nuts_code[:4]
    #nuts1 = nuts_code[:3]
    #nuts0 = nuts_code[:2]
    #return nuts3,nuts2,nuts1,nuts0
    return nuts2

def raster_array(raster, dType=float, return_gt=False):
    ds = gdal.Open(raster)
    geo_transform = ds.GetGeoTransform()
    band1 = ds.GetRasterBand(1)
    arr = band1.ReadAsArray().astype(dType)
    ds = None
    if return_gt:
        return (arr, geo_transform),None  # 0..x,1...xres,3..y,5...yres
    else:
        return arr
    
def return_nuts_codes(path_to_raster):
    code_list = pd.read_csv(path_nuts_code)
    code_list = code_list.set_index("id")["nuts_code"]
    arr = raster_array(path_to_raster)
    arr = arr.astype(int)
    # determine nuts3 codes in the raster
    unique_val, counts = np.unique(arr[arr!=0] ,return_counts=True)
    # In case of region selection from several NUTS 3 areas, only the one with
    # highest number of elements is selected.
    code = unique_val[counts.argmax()]
    nuts2_codes = []
    for i, code in enumerate(unique_val):
        # skip overlapping pixels: smallest nuts3 has an area of 1300 ha
        if counts[i] > 1290:
            nuts2_codes.append(get_nuts(code_list[int(code)]))
    # remove repeated nuts2 codes obtained from nuts3 codes
    nuts2_codes = list(set(nuts2_codes))
    return nuts2_codes

