import pandas as pd
import os

from pandas import DataFrame

DATA_DIR = "../season_1_sad/"
UPSET_DIR = "../season_1_upset/"

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"

# all the data dir we want to solve
CLUSTER_MAP_SHEET_DIR = "cluster_map"
ORDER_SHEET_DIR = "order_data"
TRAFFIC_SHEET_DIR = "traffic_data"
WEATHER_SHEET_DIR = "weather_data"
POI_SHEET_DIR = "poi_data"

def extract_poi_feature(poi_data):
    poi_sum = poi_data.sum(axis=0)[1:]
    poi_sum.columns=["district","poi_sum"]
    print(poi_sum)
    return poi_data
    


if __name__ == '__main__':
    poi_path = os.path.join(DATA_DIR, CONCRETE_DIR,POI_SHEET_DIR)
    poi_data = pd.read_csv(poi_path+"/poi_data.csv")
    extract_poi_feature(poi_data)