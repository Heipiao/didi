import pandas as pd
import numpy as np
from random import sample
import os

DATA_DIR = "../season_1_sad/"
UPSET_DIR = "../season_1_upset/"
HAPPY_DIR = "../season_1_happy/"

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"

# all the data dir we want to solve
DATA_FINAL_DIR ="feature_data_final"
TEST_WORKINGDAY = "test_workingday"


def big_order_dir(needed_map_dir):
    df = pd.DataFrame()
    if not os.path.isdir(needed_map_dir) or not os.path.exists(needed_map_dir):
        raise IOError("ERROR: " + needed_map_dir + " not existed or its not a dir")
    print("append final features sheet... in " + needed_map_dir)
    for file in os.listdir(needed_map_dir):
        if ".csv" in file:
            file_path = os.path.join(needed_map_dir, file)
            # map all the district into concrete value
            data = pd.read_csv(file_path)
            # change the file
            df = df.append(data)
            
    return df

def shift_time_series(df):
    df['passenger_num_less_cab_taker_20'] = df['passenger_num_less_cab_taker_10'].shift(1)
    df['passenger_num_high_cab_taker_20'] = df['passenger_num_high_cab_taker_10'].shift(1)
    df['passenger_num_random_cab_taker_20'] = df['passenger_num_random_cab_taker_10'].shift(1) 
    df['passenger_num_coummter_cab_taker_20'] = df['passenger_num_coummter_cab_taker_10'].shift(1)

    df['passenger_num_many_start_taker_20'] = df['passenger_num_many_start_taker_10'].shift(1) 
    df['passenger_num_less_start_taker_20'] =  df['passenger_num_less_start_taker_10'].shift(1)
    df['passenger_num_many_dest_taker_20'] =  df['passenger_num_many_dest_taker_10'].shift(1)
    df['passenger_num_less_dest_taker_20'] = df['passenger_num_less_dest_taker_10'].shift(1)

    df['passenger_num_less_cab_taker_30'] = df['passenger_num_less_cab_taker_10'].shift(2)
    df['passenger_num_high_cab_taker_30'] = df['passenger_num_high_cab_taker_10'].shift(2)
    df['passenger_num_random_cab_taker_30'] = df['passenger_num_random_cab_taker_10'].shift(2) 
    df['passenger_num_coummter_cab_taker_30'] = df['passenger_num_coummter_cab_taker_10'].shift(2)

    df['passenger_num_many_start_taker_30'] = df['passenger_num_many_start_taker_10'].shift(2) 
    df['passenger_num_less_start_taker_30'] =  df['passenger_num_less_start_taker_10'].shift(2)
    df['passenger_num_many_dest_taker_30'] =  df['passenger_num_many_dest_taker_10'].shift(2)
    df['passenger_num_less_dest_taker_30'] = df['passenger_num_less_dest_taker_10'].shift(2)

    df['passenger_num_less_cab_taker_40'] = df['passenger_num_less_cab_taker_10'].shift(3)
    df['passenger_num_high_cab_taker_40'] = df['passenger_num_high_cab_taker_10'].shift(3)
    df['passenger_num_random_cab_taker_40'] = df['passenger_num_random_cab_taker_10'].shift(3) 
    df['passenger_num_coummter_cab_taker_40'] = df['passenger_num_coummter_cab_taker_10'].shift(3)

    df['passenger_num_many_start_taker_40'] = df['passenger_num_many_start_taker_10'].shift(3) 
    df['passenger_num_less_start_taker_40'] =  df['passenger_num_less_start_taker_10'].shift(3)
    df['passenger_num_many_dest_taker_40'] =  df['passenger_num_many_dest_taker_10'].shift(3)
    df['passenger_num_less_dest_taker_40'] = df['passenger_num_less_dest_taker_10'].shift(3)

    del df['passenger_num_less_cab_taker_10']
    del df['passenger_num_high_cab_taker_10']
    del df['passenger_num_random_cab_taker_10']
    del df['passenger_num_coummter_cab_taker_10']

    del df['passenger_num_many_start_taker_10']
    del df['passenger_num_less_start_taker_10']
    del df['passenger_num_many_dest_taker_10']
    del df['passenger_num_less_dest_taker_10']

    df['driver_num_less_didi_use_20'] = df['driver_num_less_didi_use_10'].shift(1)
    df['driver_num_more_didi_use_20'] = df['driver_num_more_didi_use_10'].shift(1)

    df['driver_num_stable_loc_driver_20'] = df['driver_num_stable_loc_driver_10'].shift(1)
    df['driver_num_random_loc_driver_20'] = df['driver_num_random_loc_driver_10'].shift(1)

    df['driver_num_cheat_20'] = df['driver_num_cheat_10'].shift(1)

    df['driver_num_less_didi_use_30'] = df['driver_num_less_didi_use_10'].shift(2)
    df['driver_num_more_didi_use_30'] = df['driver_num_more_didi_use_10'].shift(2)

    df['driver_num_stable_loc_driver_30'] = df['driver_num_stable_loc_driver_10'].shift(2)
    df['driver_num_random_loc_driver_30'] = df['driver_num_random_loc_driver_10'].shift(2)

    df['driver_num_cheat_30'] = df['driver_num_cheat_10'].shift(2)

    df['driver_num_less_didi_use_40'] = df['driver_num_less_didi_use_10'].shift(3)
    df['driver_num_more_didi_use_40'] = df['driver_num_more_didi_use_10'].shift(3)

    df['driver_num_stable_loc_driver_40'] = df['driver_num_stable_loc_driver_10'].shift(3)
    df['driver_num_random_loc_driver_40'] = df['driver_num_random_loc_driver_10'].shift(3)

    df['driver_num_cheat_40'] = df['driver_num_cheat_10'].shift(3)

    del df['driver_num_less_didi_use_10']
    del df['driver_num_more_didi_use_10']

    del df['driver_num_stable_loc_driver_10']
    del df['driver_num_random_loc_driver_10']

    del df['driver_num_cheat_10']

    df["NULL_20"] = df["NULL"].shift(1) 
    df["NULL_30"] = df["NULL"].shift(2) 
    df["NULL_40"] = df["NULL"].shift(3) 


    df["null_1_20"] = df["null_1"].shift(1) 
    df["null_1_30"] = df["null_1"].shift(2) 
    df["null_1_40"] = df["null_1"].shift(3) 
    del df["null_1"]

    df["order_count_20"] = df["order_count"].shift(1) 
    df["order_count_30"] = df["order_count"].shift(2) 
    df["order_count_40"] = df["order_count"].shift(3) 


    df["tj_level1_count_20"] = df["tj_level1_count"].shift(1) 
    df["tj_level1_count_30"] = df["tj_level1_count"].shift(2) 
    df["tj_level1_count_40"] = df["tj_level1_count"].shift(3) 
    del df["tj_level1_count"]

    df["tj_level2_count_20"] = df["tj_level2_count"].shift(1) 
    df["tj_level2_count_30"] = df["tj_level2_count"].shift(2) 
    df["tj_level2_count_40"] = df["tj_level2_count"].shift(3) 
    del df["tj_level2_count"]

    df["tj_level3_count_20"] = df["tj_level3_count"].shift(1) 
    df["tj_level3_count_30"] = df["tj_level3_count"].shift(2) 
    df["tj_level3_count_40"] = df["tj_level3_count"].shift(3) 
    del df["tj_level3_count"]

    df["tj_level4_count_20"] = df["tj_level4_count"].shift(1) 
    df["tj_level4_count_30"] = df["tj_level4_count"].shift(2) 
    df["tj_level4_count_40"] = df["tj_level4_count"].shift(3) 
    del df["tj_level4_count"]

    del df["index"]



def split_train_test_set(df):
    def make_index(num):
        start = 9504 * (num-1)
        end = 9504 * (num)
        return  list(range(start,end))

    def random_index(dfr):
        rows = np.random.choice(dfr.index.values, len(dfr.index))
        dfr = dfr.ix[rows]
        return dfr

    test_workingday =  make_index(5) + make_index(13) + make_index(19)
 
    train_workingday =  make_index(4) + make_index(6) + make_index(7) +make_index(7) + make_index(11) + make_index(12)+make_index(14) + make_index(15) + make_index(18) + make_index(20) 
    test_dayoff =  make_index(2) + make_index(17) 
    train_dayoff =  make_index(3) + make_index(9) + make_index(10) + make_index(16) 
    
    directory =  os.path.join(HAPPY_DIR, CONCRETE_DIR)
    if not os.path.exists(directory):
        os.makedirs(directory)

    dfr = pd.DataFrame()
    dfr = df.iloc[test_workingday]
    dfr = random_index(dfr)
    test_workingday_path =  os.path.join(HAPPY_DIR, CONCRETE_DIR)+"/test_workingday.csv"
    dfr.to_csv(test_workingday_path,index=False)
    print(dfr.head())

    dfr = pd.DataFrame()
    dfr = df.iloc[train_workingday]
    dfr = random_index(dfr)
    train_workingday_path =  os.path.join(HAPPY_DIR, CONCRETE_DIR)+"/train_workingday.csv"
    dfr.to_csv(train_workingday_path,index=False)
    print(dfr.head())
  
    dfr = pd.DataFrame()
    dfr = df.iloc[test_dayoff]
    dfr = random_index(dfr)
    test_dayoff_path =  os.path.join(HAPPY_DIR, CONCRETE_DIR)+"/test_dayoff.csv"
    dfr.to_csv(test_dayoff_path,index=False)
    print(dfr.head())

    dfr = pd.DataFrame()
    dfr = df.iloc[train_dayoff]
    dfr = random_index(dfr)
    train_dayoff_path =  os.path.join(HAPPY_DIR, CONCRETE_DIR)+"/train_dayoff.csv"
    dfr.to_csv(train_dayoff_path,index=False)
    print(dfr.head())
  


if __name__ == '__main__':
    needed_map_dir = os.path.join(UPSET_DIR, CONCRETE_DIR,DATA_FINAL_DIR)
    #combine_weather_order_traffic(needed_map_dir)
    df = pd.DataFrame()
    df = big_order_dir(needed_map_dir)
    shift_time_series(df)
    df.index = range(1,len(df) + 1)
    df.fillna(0)
    split_train_test_set(df)
  



