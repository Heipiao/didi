#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-24 01:11:01
# @Author  : chensijia (2350543676@qq.com)
# @Version : 0.0.0
# @Style   : Python3.4
#
# @Description: 




## import python`s own lib
import os
from collections import OrderedDict

## import third party lib
import pandas as pd
import numpy

## import local lib



DATA_DIR = "../season_1_sad/" # only change this dir to change the operate dir

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"

## all the data dir we want to solve
TRAFFIC_SHEET_DIR = "traffic_data"


##############################################################################
###################### analysis traffic data here ##########################
def is_repeat_time_sheet(df):
    repeat_time_districts = OrderedDict()
    for d in df.district.unique():
        district_time = df[df.district == d].time_slices
        ## if there is a repeat itme slice
        if district_time.duplicated().any():
            repeat_time_districts[d] = list(district_time[district_time.duplicated()])
    return repeat_time_districts

def what_time_missed(df_time):
    normal_time_slice = list(range(1, 145))
    for time_slice in df_time:
        if time_slice in normal_time_slice:
            normal_time_slice.remove(time_slice)
    if normal_time_slice:
        return normal_time_slice
    else:
        return None

def is_miss_time_sheet(df):
    if "district" in df.columns:
        sheet_district = df.district
    elif "start_district" in df.columns:
        sheet_district = df.start_district
    else:
        ## this sheet does not contain district
        # print("******* not district contained ************")
        current_time_slices = df["time_slices"].unique()
        missed_time = what_time_missed(current_time_slices)
        if missed_time:
            return missed_time
        else:
            return None
    # key is the contain miss time district, value is what time missed
    miss_time_district = OrderedDict()
    for d in sheet_district.unique():
        district_time = df[sheet_district == d].time_slices
        # if there is a miss item slice
        if district_time.unique().shape[0] < 144:
            miss_time_district[d] = what_time_missed(district_time.unique())
    if miss_time_district:
        return miss_time_district
    else:
        return None



def is_miss_district_sheet(df):
    print("analysising missing district......")
    miss_district = list(range(1, 67))
    if "district" in df.columns:
        district_uni = df.district.unique()
    elif "start_district" in df.columns:
        district_uni = df.start_district.unique()

    # print(district_uni.shape[0])
    if district_uni.shape[0] <= 66:
        for d in district_uni:
            miss_district.remove(d)
    if miss_district:
        return miss_district
    else:
        return None


judge_function = {"is_repeat_time": is_repeat_time_sheet,
                  "is_miss_time": is_miss_time_sheet,
                  "is_miss_district": is_miss_district_sheet}
def contain_bad_sheet_dir(needed_judge_dir, judge_what = "is_repeat_time"):
    if not os.path.isdir(needed_judge_dir) or not os.path.exists(needed_judge_dir):
        raise IOError("ERROR: " + needed_judge_dir + " not existed or its not a dir")

    print("visit all the sheets... in " + needed_judge_dir)
    dates = dict()
    for file in os.listdir(needed_judge_dir):
        if ".csv" in file:
            file_path = os.path.join(needed_judge_dir, file)
            # map all the district into concrete value
            df = pd.read_csv(file_path)
            judge = judge_function[judge_what]

            judge_result = judge(df)
            dates[str(df.date.unique()[0])] = judge_result
    dates = OrderedDict(sorted(dates.items(), key=lambda d:d[0]))
    return dates
            # change the file

################################################################################
####################### order data analysis ####################################
# input:
def count_district_time_order(df):
    current_date = df.date.unqiue()
    

def count_order_dir(order_data_dir):
    pass


if __name__ == '__main__':
    data_frame = pd.read_csv(os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR, 
                        "traffic_data_2016-01-01.csv"))
    repeat_time_districts=is_miss_time_sheet(data_frame)
    print(repeat_time_districts)
    missed_district = is_miss_district_sheet(data_frame)
    print(missed_district)