#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-03 22:59:49
# @Author  : chensijia (2350543676@qq.com)
# @Version : 0.0.0
# @Style   : Python3.4
#
# @Description: 




## import python`s own lib
import os
from functools import reduce  
from collections import OrderedDict

## import third party lib
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean

## import local lib




DATA_DIR = "../season_1_sad/" # only change this dir to change the operate dir

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"


TRAFFIC_SHEET_DIR = "traffic_data"


'''
Aftering analysising the traffic data, we found that:
1. there is no missing districts in any date...
2. 2016-06-20: missing many time slices && every district missing the same time slices
3. rest of the date only miss the time slices 1 in every district

'''

special_missing_time_slices_date = ["20"]
# [1, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 
#   124, 129, 130, 131, 132, 133, 134, 135, 136, 137]


### because the special case of traffic time missing
## simple fill with time slices previous day`s 144 and current date`s 2 ...
def filling_missing_time_with_neighbor_one(df, previous_date_df):
    time_slices_num = 144

    if previous_date_df.empty:
        previous_date_df = df.copy()
        time_slices_num = 2

    splited_df = df.groupby(by = ["district", "time_slices"])
    splited_pre_df = previous_date_df.groupby(by = ["district", "time_slices"])

    for d in df.district.unique():
        ts2_d_group = splited_df.get_group((d, 2))
        pre_ts144_d_group = splited_pre_df.get_group((d, time_slices_num))

        temp = ts2_d_group.copy()
        ## we set its correspond value as mean
        temp.iat[0, 1] = np.mean([ts2_d_group.iat[0, 1], pre_ts144_d_group.iat[0, 1]])
        temp.iat[0, 2] = np.mean([ts2_d_group.iat[0, 2], pre_ts144_d_group.iat[0, 2]])
        temp.iat[0, 3] = np.mean([ts2_d_group.iat[0, 3], pre_ts144_d_group.iat[0, 3]])
        temp.iat[0, 4] = np.mean([ts2_d_group.iat[0, 4], pre_ts144_d_group.iat[0, 4]])
        # set its time slices as 1
        temp.iat[0, 8] = 1
        
        Time = temp.iat[0, 5].strip().split("-")
        Time[-1] = str(1)
        Time = reduce(lambda x, y: x + "-" + y, Time)
        temp.iat[0, 5] = Time

        df = df.append(temp)
    return df


## this function fill the missing time slices
##      --> only concentrate on the date missing time slices 1 in every district
def filling_traffic_common_time_missing_dir(traffic_data_dir):
    print("filling missing time slices 1 in traffic data")
    previous_date_df = pd.DataFrame()
    for tf in sorted(os.listdir(traffic_data_dir)):
        if ".csv" in tf:
            print("processing: ", tf)
            file_path = os.path.join(traffic_data_dir, tf)
            now_date_df = pd.read_csv(file_path)
            if not 1 in now_date_df.time_slices.unique():
                df = filling_missing_time_with_neighbor_one(now_date_df, previous_date_df)

                df.to_csv(file_path, index = False)

                previous_date_df = df.copy()


# this function aim to filling the time slices missing in all district
## we think that the date:
#   01 02 04 05 06 07 09 10 11 13 14 15 16 17 18 19 21
#   16 10 --> contain 4 continue missing
#   03 08 12
#   20
'''
Note: for date 20 --> its friday same as date 06, date 13
        we make use of which one is the most same as date 20 
        beforing time slices missed...
'''
def filling_missing_time_with_neighbors(df, dis_group, ts_l1_c, ts_l2_c, ts_l3_c, ts_l4_c):
    # print(ts_l1_c)
    # print(ts_l3_c)
    # print(dis_group)
    # 2016-01-01-144
    next_ts = 0
    pre_ts = 0
    for ts in range(ts_l1_c.shape[0]):
        if ts_l1_c[ts] == -1: # here is a missing time slices
            temp = dis_group.copy() # the missing ts information we want to add to df
            temp.iat[0, 8] = ts + 1 # set its time slices as the missing one

            # change the Time
            Time = temp.iat[0, 5].strip().split("-")
            Time[-1] = str(ts + 1)
            Time = reduce(lambda x, y: x + "-" + y, Time)
            temp.iat[0, 5] = Time

            pre_ts = ts - 1
            next_ts = ts + 1
            if not ts_l1_c[next_ts] == -1:
                ts_l1_c[ts] = int(ts_l1_c[pre_ts] + (ts_l1_c[next_ts] - ts_l1_c[pre_ts])/2)
                ts_l2_c[ts] = int(ts_l2_c[pre_ts] + (ts_l2_c[next_ts] - ts_l2_c[pre_ts])/2)
                ts_l3_c[ts] = int(ts_l3_c[pre_ts] + (ts_l3_c[next_ts] - ts_l3_c[pre_ts])/2)
                ts_l4_c[ts] = int(ts_l4_c[pre_ts] + (ts_l4_c[next_ts] - ts_l4_c[pre_ts])/2)
            else:
                ts_l1_c[ts] = ts_l1_c[pre_ts]
                ts_l2_c[ts] = ts_l2_c[pre_ts]
                ts_l3_c[ts] = ts_l3_c[pre_ts]
                ts_l4_c[ts] = ts_l4_c[pre_ts]

            temp.iat[0, 1] = ts_l1_c[ts]
            temp.iat[0, 2] = ts_l2_c[ts]
            temp.iat[0, 3] = ts_l3_c[ts]
            temp.iat[0, 4] = ts_l4_c[ts]
            #print(temp)
            df = df.append(temp)
    return df


def get_dis_ts_lv_count(df, d):
    d_t_group = df.groupby(by = ["district", "time_slices"])
    ## get its time slices situation
    ts_l1_c = -1 * np.ones((144,))
    ts_l2_c = -1 * np.ones((144,))
    ts_l3_c = -1 * np.ones((144,))
    ts_l4_c = -1 * np.ones((144,))
    for (dis, dis_ts), group in d_t_group:
        if dis == d:
            ts_l1_c[dis_ts - 1] = group.iat[0, 1]
            ts_l2_c[dis_ts - 1] = group.iat[0, 2]
            ts_l3_c[dis_ts - 1] = group.iat[0, 3]
            ts_l4_c[dis_ts - 1] = group.iat[0, 4]
            dis_group = group

    return ts_l1_c, ts_l2_c, ts_l3_c, ts_l4_c, dis_group

def filling_missing_time_slice_type1_date(df):
    # visiting all the district, and its responding time slices
    for d in df.district.unique():
        ts_l1_c, ts_l2_c, ts_l3_c, ts_l4_c, dis_group = get_dis_ts_lv_count(df, d)          
        if -1 in ts_l1_c:
            df = filling_missing_time_with_neighbors(df, dis_group, ts_l1_c, ts_l2_c, ts_l3_c, ts_l4_c)

    return df

#01 02 04 05 06 07 09 10 11 13 14 15 16 17 18 19 21
#   03 08 12
type1_date = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",
            "13", "14", "15", "16", "17", "18", "19", "21"]
def filling_missing_time_slice_type1_dir(traffic_data_dir):
    print("filling missing time slices in traffic data:")
    for tf in sorted(os.listdir(traffic_data_dir)):
        if not "~" in tf and ".csv" in tf and tf.strip().split("-")[-1][:2] in type1_date:
            print("processing: ", tf)
            df = pd.read_csv(os.path.join(traffic_data_dir, tf))
            df = filling_missing_time_slice_type1_date(df)

            df.to_csv(os.path.join(traffic_data_dir, tf), index = False)


## Note : use this function to solve the date 20
#           --> date 20: missing too many continue time slices
## date 06 13 is the same week as date 20...
## 

type2_date = ["20"]
work_days = ["04", "05", "06", "07", "08", "11", "12", "13", "14", "18", "19",
            "21", "15"]

def compare_lv(d, df, date_df):
    # get the date 20
    ts_l1_c, ts_l2_c, ts_l3_c, ts_l4_c, dis_group = get_dis_ts_lv_count(df, d)
    #print(ts_l1_c)
    flag = 1

    ts_nearest_date = OrderedDict()

    for ts in range(ts_l1_c.shape[0]):
        if ts_l1_c[ts] == -1:
            if flag == 0:
                continue
            ## find next non -1 value respond tiem slices
            need_calculate_ts = 0
            for next_tss in range(ts + 1, ts_l1_c.shape[0]):
                if not ts_l1_c[next_tss] == -1:
                    need_calculate_ts = next_tss
                    #print("oo: ", need_calculate_ts)
                    break

            #print("time: ", ts)
            based_ts_l1_c = ts_l1_c[ts - 3 : ts]
            based_ts_l2_c = ts_l2_c[ts - 3 : ts]
            based_ts_l3_c = ts_l3_c[ts - 3 : ts]
            based_ts_l4_c = np.concatenate((ts_l4_c[ts - 3 : ts],ts_l4_c[need_calculate_ts: need_calculate_ts + 3]))
            #print(based_ts_l4_c)
            dis_result = OrderedDict()
            dis_result[df.date.unique()[0]] = OrderedDict()
            for k, v in date_df.items():
                date_ts_l1_c, date_ts_l2_c, date_ts_l3_c, date_ts_l4_c, g = get_dis_ts_lv_count(v, d)
                compare_ts_l1_c = date_ts_l1_c[ts - 3 : ts]
                compare_ts_l2_c = date_ts_l2_c[ts - 3 : ts]
                compare_ts_l3_c = date_ts_l3_c[ts - 3 : ts]
                compare_ts_l4_c = np.concatenate((date_ts_l4_c[ts - 3 : ts],date_ts_l4_c[need_calculate_ts: need_calculate_ts + 3]))

                #print(k, compare_ts_l4_c)
                dis_result[df.date.unique()[0]][k[:2]] = euclidean(based_ts_l4_c, compare_ts_l4_c)
                #print(dis_result[df.date.unique()[0]][k[:2]])
            dis_result[df.date.unique()[0]] = OrderedDict(sorted(dis_result[df.date.unique()[0]].items(), key=lambda d:d[1]))
            ## add the nearest to

            #print(dis_result[df.date.unique()[0]])
            for dis_date_k in dis_result[df.date.unique()[0]].keys():
                ts_nearest_date[ts] = dis_date_k
                break
            #print(dis_result)
            flag = 0
        else:
            flag = 1

    #print(ts_nearest_date)
    return ts_nearest_date

def replace_with_new(start_ts, ts_ln_c, replace_ts_ln_c):
    end_ts = start_ts
    for ts in range(start_ts + 1, ts_ln_c.shape[0]):
        if not ts_ln_c[ts] == -1:
            end_ts = ts
            break
    ts_ln_c[start_ts:end_ts] = replace_ts_ln_c[start_ts:end_ts]

def filling_missing_time_with_nearest_day(d, df, ts_nearest_date, date_df):
    ts_l1_c, ts_l2_c, ts_l3_c, ts_l4_c, dis_group = get_dis_ts_lv_count(df, d)

    get_replace_flag = 0
    for ts in range(ts_l1_c.shape[0]):
        if ts_l1_c[ts] == -1:
            if not get_replace_flag:
                replace_ts_l1_c,replace_ts_l2_c,replace_ts_l3_c,replace_ts_l4_c, g = get_dis_ts_lv_count(date_df[ts_nearest_date[ts]], d)
                #print(ts_nearest_date[ts], replace_ts_l1_c)

            temp = dis_group.copy() # the missing ts information we want to add to df
            temp.iat[0, 8] = ts + 1 # set its time slices as the missing one
            # change the Time
            Time = temp.iat[0, 5].strip().split("-")
            Time[-1] = str(ts + 1)
            Time = reduce(lambda x, y: x + "-" + y, Time)
            temp.iat[0, 5] = Time

            temp.iat[0, 1] = replace_ts_l1_c[ts]
            temp.iat[0, 2] = replace_ts_l2_c[ts]
            temp.iat[0, 3] = replace_ts_l3_c[ts]
            temp.iat[0, 4] = replace_ts_l4_c[ts]

            get_replace_flag = 1

            df = df.append(temp)

        else:
            get_replace_flag = 0

    return df

def filling_missing_time_slice_type2_date(df, traffic_data_dir):
    ## first we read the same week date
    date_df = dict()
    for tf in os.listdir(traffic_data_dir):
        which_date = tf.strip().split("-")[-1][:2]
        if not "~" in tf and ".csv" in tf and which_date in work_days:
            date_df[which_date] = pd.read_csv(os.path.join(traffic_data_dir, tf))
    
    # visiting all the district, and its responding time slices
    for d in df.district.unique():
        print("district ",  d)
        ts_nearest_date = compare_lv(d, df, date_df)
        df = filling_missing_time_with_nearest_day(d, df, ts_nearest_date, date_df)

    return df


def filling_missing_time_slice_type2_dir(traffic_data_dir):
    print("filling missing time slices type2 date in traffic data:")
    for tf in sorted(os.listdir(traffic_data_dir)):
        if not "~" in tf and ".csv" in tf and tf.strip().split("-")[-1][:2] in type2_date:
            print("processing: ", tf)
            df = pd.read_csv(os.path.join(traffic_data_dir, tf))
            df = filling_missing_time_slice_type2_date(df, traffic_data_dir)
            df.to_csv(os.path.join(traffic_data_dir, tf), index = False)



def process_filling_missing_dir(traffic_data_dir):
    filling_traffic_common_time_missing_dir(traffic_data_dir)
    filling_missing_time_slice_type1_dir(traffic_data_dir)
    filling_missing_time_slice_type2_dir(traffic_data_dir)

if __name__ == '__main__':
    traffic_data_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR)
    # # filling_traffic_common_time_missing_dir(traffic_data_dir)
    #df = pd.read_csv(os.path.join(traffic_data_dir, "traffic_data_2016-01-20.csv"))
    #print(df.head())
    # df = filling_missing_time_slice_type1_date(df)
    # filling_missing_time_slice_type1_dir(traffic_data_dir)

    #filling_missing_time_slice_type2_date(df, traffic_data_dir)
    filling_missing_time_slice_type2_dir(traffic_data_dir)