#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-22 23:19:06
# @Author  : chensijia (2350543676@qq.com)
# @Version : 0.0.0
# @Style   : Python3.4
#
# @Description: 


## import python`s own lib
import os

## import third party lib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## import local lib
from analysis_data import contain_bad_sheet_dir


DATA_DIR = "../season_1_sad/" # only change this dir to change the operate dir

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"

## all the data dir we want to solve
CLUSTER_MAP_SHEET_DIR = "cluster_map"
ORDER_SHEET_DIR = "order_data"
TRAFFIC_SHEET_DIR = "traffic_data"
WEATHER_SHEET_DIR = "weather_data"
POI_SHEET_DIR = "poi_data"



##############################################################################
###################### analysis traffic data here ##########################

### !!!!! Note: it is obvious that:
####             the traffic data contains missing time slice, so no judgement

def is_traffic_data_contain_repeat_time_sheet():
    traffic_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR)
    # judge whether it has repeat time sheet or not
    repeat_dates = contain_bad_sheet_dir(traffic_data_dir, judge_what = "is_repeat_time")
    if repeat_dates:
        return repeat_dates # a dict style object  date: repeat_district(list)
    else:
        return False

## -20 date: is ths most worst one
def is_traffic_data_contain_miss_time_sheet():
    print("missing time information in traffic data: date{district_num: [missed time slice]} ")
    traffic_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR)
    # judge whether it has repeat time sheet or not
    miss_dates = contain_bad_sheet_dir(traffic_data_dir, judge_what = "is_miss_time")
    if miss_dates:
        return miss_dates
    else:
        False

## After analysising: there is only missing district number 54!!!
def is_traffic_data_contain_miss_district_sheet():
    print("missing time information in traffic data: date [missed district]")
    traffic_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR)
    # judge whether it has repeat time sheet or not
    miss_dates = contain_bad_sheet_dir(traffic_data_dir, judge_what = "is_miss_district")
    if miss_dates:
        return miss_dates
    else:
        False    



##############################################################################
###################### analysis weather data here ##########################
def is_weather_data_contain_miss_time_sheet():
    print("missing time information in weather data: date [missed time slice]")
    weather_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, WEATHER_SHEET_DIR)
    # judge whether it has repeat time sheet or not
    miss_dates = contain_bad_sheet_dir(weather_data_dir, judge_what = "is_miss_time")
    if miss_dates:
        return miss_dates
    else:
        False

##############################################################################
###################### analysis order data here ##########################
## order data`s missing time slices is complex!!!
def is_order_data_contain_miss_time_sheet():
    print("missing time information in order data: date [missed time slice]")
    order_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR)
    # judge whether it has repeat time sheet or not
    miss_dates = contain_bad_sheet_dir(order_data_dir, judge_what = "is_miss_time")
    if miss_dates:
        return miss_dates
    else:
        False

## order data has no missing districts...
def is_order_data_contain_miss_district_sheet():
    print("missing time information in order data: date [missed district]")
    order_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR)
    # judge whether it has repeat time sheet or not
    miss_dates = contain_bad_sheet_dir(order_data_dir, judge_what = "is_miss_district")
    if miss_dates:
        return miss_dates
    else:
        False 

if __name__ == '__main__':
    pass
    ##################### analysis traffic data #############################
    adf = list()
    res = is_traffic_data_contain_miss_time_sheet()
    for k, v in res.items():
        print(k, v)
        #adf.extend(v[15])
    #print(sorted(list(set(adf))))
        
    res = is_traffic_data_contain_miss_district_sheet()

    for k, v in res.items():
        print(k, v)


        
    #################### analysis weather data #############################
    # res = is_weather_data_contain_miss_time_sheet()
    # for k, v in res.items():
    #      print(k, v)

    ##################### analysis order data #############################
    # res = is_order_data_contain_miss_time_sheet()
    # for k, v in res.items():
    #     print(k, v)
        # for missed_dis, missed_time_slices in v.items():
        #     print(missed_dis, len(missed_time_slices))
    # from plot_order_data import plot_missed_time_slice, plot_missed_time_slice_district
    # plot_missed_time_slice(res)
    # plot_missed_time_slice_district(res)
    
    # #### After analysising, the order does not have any missed district
    # missed_district = is_order_data_contain_miss_district_sheet()
    # for k, v in missed_district.items():
    #     print(k, v)