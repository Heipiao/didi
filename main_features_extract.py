import pandas as pd
import os

from pandas import DataFrame
from features_order_self import *
from extract_features_from_poi_data import extract_features_for_poi
from features_combined import *
from feature_big_sheet import *

LOAD_DATA_DIR = "../season_1_sad/" # only change this dir to change the operate dir
SAVE_DATA_DIR = "../season_1_upset/"
UPSET_DIR = "../season_1_upset/"
HAPPY_DIR = "../season_1_happy/"

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"

# all the data dir we want to solve
CLUSTER_MAP_SHEET_DIR = "cluster_map"
ORDER_SHEET_DIR = "order_data"
TRAFFIC_SHEET_DIR = "traffic_data"
WEATHER_SHEET_DIR = "weather_data"
POI_SHEET_DIR = "poi_data"

def extract_poi_features():
    poi_dir = os.path.join(LOAD_DATA_DIR, CONCRETE_DIR, POI_SHEET_DIR)
    featured_poi_df = extract_features_for_poi(poi_dir)

    saved_dir_path = os.path.join(SAVE_DATA_DIR, CONCRETE_DIR, POI_SHEET_DIR)
    if not os.path.exists(saved_dir_path):
        os.makedirs(saved_dir_path)
    print("saving the extracted features to: ", saved_dir_path)
    featured_poi_df.to_csv(os.path.join(saved_dir_path, "poi_features.csv"), index = False)

def extract_order_features():
    path = os.path.join(DATA_DIR, CONCRETE_DIR,ORDER_SHEET_DIR)
    features_order_dir(path)

def combine_features():
    needed_map_dir = os.path.join(UPSET_DIR, CONCRETE_DIR)
    df = combine_all_dir(needed_map_dir)

def split_train_test_set_combine_features():
    needed_map_dir = os.path.join(UPSET_DIR, CONCRETE_DIR,DATA_FINAL_DIR)
    df = pd.DataFrame()
    df = big_order_dir(needed_map_dir)
    shift_time_series(df)
    df.index = range(1,len(df) + 1)
    df.fillna(0)
    split_train_test_set(df)

if __name__ == '__main__':
	extract_poi_features()
	#extract_order_features()
	combine_features()
	split_train_test_set_combine_features()
    
