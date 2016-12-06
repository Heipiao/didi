import os

## import third party lib
import pandas as pd
import numpy as np

## import local lib


DATA_DIR = "../season_1_sad/"

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"



TRAFFIC_SHEET_DIR = "traffic_data"



#### distrcit 54 is missing in all the date

## after analysising the poi data,
## ----> find that the district 13 is the most same as district 54

# ----> so we fill the district 54 with 13
def replaced(x):
    x.district = 54
    return x

def filling_district(traffic_df):

    district_traffic_df = traffic_df[traffic_df["district"] == 13].copy()
    temp_traffic_df = district_traffic_df.apply(lambda x: replaced(x), axis = 1)

    traffic_df = traffic_df.append(temp_traffic_df)

    return traffic_df


def process_filling_district_dir(traffic_data_dir):
    print("filling missing district in traffic data...")
    for file in sorted(os.listdir(traffic_data_dir)):
        if ".csv" in file and not "~" in file:
            print("filling: ", file)
            traffic_df = pd.read_csv(os.path.join(traffic_data_dir, file))

            filled_traffic_df = filling_district(traffic_df)

            filled_traffic_df.to_csv(os.path.join(traffic_data_dir, file), index = False)



if __name__ == '__main__':
    pass