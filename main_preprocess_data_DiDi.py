#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-20 05:17:06
# @Author  : chensijia (2350543676@qq.com)
# @Version : 0.0.0
# @Style   : Python3.4
#
# @Description: preprocess the data...

## import python`s own lib
import os

## import third party lib
import pandas as pd

## import local lib
from operate_hash import district_hash_map_dir, MyDistrictHashMapDict
from operate_organize_sheet_data import organize_data_sheet_dir
from process_repeat_noise_weather_data import process_repeat_noise_weather_dir
from process_missing_traffic_time_slices import process_filling_missing_dir
from process_missing_traffic_district import process_filling_district_dir
# from process_missing_traffic_time_slices import filling_traffic_common_time_missing_dir

DATA_DIR = "../season_1_sad/"

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"



## all the data dir we want to solve
CLUSTER_MAP_SHEET_DIR = "cluster_map"
ORDER_SHEET_DIR = "order_data"
TRAFFIC_SHEET_DIR = "traffic_data"
WEATHER_SHEET_DIR = "weather_data"
POI_SHEET_DIR = "poi_data"




##############################################################################
###################### preprocess traffic data here ##########################
#### Noet: No repeat of time slices sta for one district
#### only miss district: 54   time: more....
def map_traffic_data_district_hash():
    traffic_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR)
    # map the hash in traffic data
    district_hash_map_dir(traffic_data_dir)

## we re order the sheet as:
#   - district from 1 --> 64
#   - time slices contained in one district from 1 --> 144
def organize_traffic_data():
    traffic_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR)
    # organize the traffic sheet
    organize_data_sheet_dir(traffic_data_dir, according_to = ["district", "time_slices"])

def filling_missing_time_slices_date_traffic_data():
    traffic_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR)
    # filling three types of missing 
    process_filling_missing_dir(traffic_data_dir)

def filling_missing_district_traffic_data():
    traffic_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR)
    # filling three types of missing 
    process_filling_district_dir(traffic_data_dir)
##############################################################################
###################### preprocess weather data here ##########################

def process_weather_repeat_noise():
    weather_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, WEATHER_SHEET_DIR)
    ## do it here 
    process_repeat_noise_weather_dir(weather_data_dir)


##############################################################################
###################### preprocess poi data here ##########################
def map_poi_data_district_hash():
    poi_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, POI_SHEET_DIR)
    ## do it here 
    district_hash_map_dir(poi_data_dir)

def organize_poi_data():
    poi_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, POI_SHEET_DIR)
    ## do it here 
    organize_data_sheet_dir(poi_data_dir, according_to = "district")
##############################################################################
###################### preprocess order data here ##########################
def map_order_data_district_hash():
    order_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR)
    # map the hash in traffic data
    district_hash_map_dir(order_data_dir)

# def organize_order_data():
#     order_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR)
#     # organize the traffic sheet
#     organize_data_sheet_dir(order_data_dir, according_to = ["start_district", "time_slices"])

      


if __name__ == '__main__':
    # ######################## traffic data pre process ##################
    map_traffic_data_district_hash()
    filling_missing_time_slices_date_traffic_data()
    filling_missing_district_traffic_data()
    organize_traffic_data()

    # 
    ####################### weather data pre process ##################
    #process_weather_repeat_noise()
    
    # # ####################### poi data pre process ##################
    # map_poi_data_district_hash()
    # organize_poi_data()

    # # ####################### order data pre process ######################
    # # ##
    # # ## ap all the district col in the order sheet to value
    # map_order_data_district_hash()
    # organize_order_data()