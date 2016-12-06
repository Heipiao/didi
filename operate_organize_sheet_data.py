#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-23 23:40:14
# @Author  : chensijia (2350543676@qq.com)
# @Version : 0.0.0
# @Style   : Python3.4
#
# @Description: 




## import python`s own lib
import os


## import third party lib
import pandas as pd
import numpy as np

## import local lib



DATA_DIR = "../season_1_sad/" # only change this dir to change the operate dir

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"

## all the data dir we want to solve
CLUSTER_MAP_SHEET_DIR = "cluster_map"
ORDER_SHEET_DIR = "order_data"
TRAFFIC_SHEET_DIR = "traffic_data"
WEATHER_SHEET_DIR = "weather_data"
POI_SHEET_DIR = "poi_data"



# the input df is one traffice sheet needed to organized
# according_to = ["district", "time_slices"]
def organize_data_sheet(df, according_to):
    organized_df = df.sort_values(by = according_to)

    # organized_df = organized_df[organized_df.district == 1]
    # print(organized_df)
    # print(organized_df["district"].unique())
    return organized_df


def organize_data_sheet_dir(needed_map_dir, according_to):
    if not os.path.isdir(needed_map_dir) or not os.path.exists(needed_map_dir):
        raise IOError("ERROR: " + needed_map_dir + " not existed or its not a dir")
    print("organize all the sheet... in " + needed_map_dir)
    for file in os.listdir(needed_map_dir):
        if ".csv" in file:
            file_path = os.path.join(needed_map_dir, file)
            # map all the district into concrete value
            organized_data_frame = organize_data_sheet(pd.read_csv(file_path), according_to)
            # change the file
            organized_data_frame.to_csv(file_path, index = False)

if __name__ == '__main__':
    data_frame = pd.read_csv(os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR, 
                            "traffic_data_2016-01-17.csv"))
    #print(data_frame.head(50))
    #print(data_frame["district"].unique().shape)

    data_frame = organize_data_sheet(data_frame)
    