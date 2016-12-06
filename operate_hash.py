#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-20 17:00:40
# @Author  : chensijia (2350543676@qq.com)
# @Version : 0.0.0
# @Style   : Python3.4
#
# @Description: operate the hash style features

# pd.DataFrame(d.items())  # or list(d.items())


## import python`s own lib
import os
import re
import pickle
from itertools import chain
from collections import OrderedDict

## import third party lib
import pandas as pd

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



class MyDistrictHashMapDict(dict):
    def __missing__(self, key):
        self[key] = max(self.values()) + 1
        return self[key]

class MyIDHashMapDict(dict):
    def __missing__(self, key):
        if not len(list(self.values())) == 0:
            self[key] = max(self.values()) + 1
        else:
           self[key] = 1 
        return self[key]

def create_hash_district_map_dict():
    print("creating map rule...")
    file = "cluster_map.csv"
    district_hash_map_path = os.path.join(DATA_DIR, CONCRETE_DIR, CLUSTER_MAP_SHEET_DIR, file)

    hash_data = pd.read_csv(district_hash_map_path)
    ## convert the dataframe into dict
    hash_map_rule = MyDistrictHashMapDict(zip(hash_data.district_hash, hash_data.district_map))
    
    #print(type(hash_map_rule))

    saved_file = "cluster_map.pickle"
    map_save_file = os.path.join(DATA_DIR, CONCRETE_DIR, CLUSTER_MAP_SHEET_DIR, saved_file)
    ## save into same dir as file
    with open(map_save_file, "wb") as f:
        pickle.dump(hash_map_rule, f)

    #print(hash_map_rule)


def map_additional(x, map_rule):
    if type(x) == str:
        x = map_rule[x]
    return x

# map the district features in the input data_frame into value
def district_hash_map(data_frame):
    district_map_f = "cluster_map.pickle"
    district_map_f_path = os.path.join(DATA_DIR, CONCRETE_DIR, CLUSTER_MAP_SHEET_DIR, 
                                        district_map_f)
    if not os.path.exists(district_map_f_path):
        print("not existed, so we create one")
        create_hash_district_map_dict()
        # load the needed map file
    
    map_rule = MyDistrictHashMapDict()
    with open(district_map_f_path, "rb") as f:
        map_rule = pickle.load(f)

    print("map_rule: ", type(map_rule))
    # map the needed cols..
    for i in range(len(data_frame.columns)):
        if "district_hash" in data_frame.columns[i]:
            # map the hash according to the map rule
            district_hash_col = data_frame.columns[i]
            data_frame[district_hash_col] = data_frame[district_hash_col].replace(map_rule)
            #print(type(data_frame[district_hash_col][23]))
            # ## solve the district hash that not mapped
            data_frame[district_hash_col] = data_frame[district_hash_col].apply(lambda x: map_additional(x, map_rule))
            # after mapping, delete its hash str
            new_name = re.sub("_hash","",district_hash_col)
            data_frame.rename(columns={district_hash_col: new_name}, inplace = True)

    with open(district_map_f_path, "wb") as f:
        pickle.dump(map_rule, f)
    return data_frame


## input the dir you want to map the hash
def district_hash_map_dir(needed_map_dir):
    if not os.path.isdir(needed_map_dir) or not os.path.exists(needed_map_dir):
        raise IOError("ERROR: " + needed_map_dir + " not existed or its not a dir")
    print("mapping all the district... in " + needed_map_dir)
    for file in os.listdir(needed_map_dir):
        if ".csv" in file:
            file_path = os.path.join(needed_map_dir, file)
            # map all the district into concrete value
            mapped_data_frame = district_hash_map(pd.read_csv(file_path))
            # change the file
            mapped_data_frame.to_csv(file_path, index = False, na_rep = "NULL")




###################### id hash map #################################

### we should distinguish the:
# - order_id
# - driver_id
# - passenger_id
## according to the input: map_rule_name(str only)

def id_hash_map(data_frame, map_rule_name):
    print("need to map: " + map_rule_name)

    saved_file = map_rule_name + ".pickle"
    id_map_f_path = os.path.join(DATA_DIR, CONCRETE_DIR, CLUSTER_MAP_SHEET_DIR, saved_file)
    id_map_rule = MyIDHashMapDict()
    # this data_frame is the one needed to be mapped
    if map_rule_name in data_frame.columns:
        # load the needed map file
        if os.path.exists(id_map_f_path):
            with open(id_map_f_path, "rb") as f:
                id_map_rule = pickle.load(f)


        # map the needed cols..
        for i in range(len(data_frame.columns)):
            if map_rule_name == data_frame.columns[i]:
                print("mapping id: ", map_rule_name)
                # map the hash according to the map rule
                id_hash_col = data_frame.columns[i]
                
                if id_map_rule:
                    # map the id --> value contained in the map rule
                    data_frame[id_hash_col] = data_frame[id_hash_col].replace(id_map_rule)
                    # map the additional
                    data_frame[id_hash_col] = data_frame[id_hash_col].apply(lambda x: map_additional(x, id_map_rule))
                else:
                    data_frame[id_hash_col] = data_frame[id_hash_col].apply(lambda x: map_additional(x, id_map_rule))
                # after mapping, delete its hash str
                new_name = re.sub("_id","",id_hash_col)
                data_frame.rename(columns={id_hash_col: new_name}, inplace = True)
    with open(id_map_f_path, "wb") as f:
        pickle.dump(id_map_rule, f)
    return data_frame


def id_hash_map_dir(needed_map_dir, map_rule_name):
    if not os.path.isdir(needed_map_dir) or not os.path.exists(needed_map_dir):
        raise IOError("ERROR: " + needed_map_dir + " not existed or its not a dir")
    print("mapping all the id... in " + needed_map_dir)
    for file in os.listdir(needed_map_dir):
        if ".csv" in file:
            file_path = os.path.join(needed_map_dir, file)
            # map all the district into concrete value
            mapped_data_frame = id_hash_map(pd.read_csv(file_path), map_rule_name)
            # change the file
            mapped_data_frame.to_csv(file_path, index = False, na_rep = "NULL")


if __name__ == '__main__':
    ################# traffic data district hash map ###############
    # data_frame = pd.read_csv(os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR, 
    #                         "traffic_data_2016-01-01.csv"))
    # data_frame = district_hash_map(data_frame)
    # print(data_frame)
    # district_hash_map_dir()



    ################ order data district hash map ###################
    data_frame = pd.read_csv(os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR, 
                            "order_data_2016-01-01.csv"))
#    data_frame = district_hash_map(data_frame)
    data_frame = id_hash_map(data_frame, "passenger_id")
    print(data_frame)
    # data_frame = pd.read_csv(os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR, 
    #                         "order_data_2016-01-01.csv"))
    # df = district_hash_map(data_frame)
    # print(df) 
    # df.to_csv("asdfdsffsdasdaf.csv", index = False, na_rep = "NULL")
