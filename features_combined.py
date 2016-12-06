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

def combine_all_dir(needed_map_dir):
	# if not os.path.isdir(needed_map_dir) or not os.path.exists(needed_map_dir):
 #        raise IOError("ERROR: " + needed_map_dir + " not existed or its not a dir")
    df = pd.DataFrame()
    print("combinall sheet... in " + needed_map_dir)
    for day in range(1,22):
        if day <10 :
            name =  "2016-01-"+"0"+str(day)+".csv"
        else:
            name =  "2016-01-"+str(day)+".csv"
        print(name)
      
        print("process data on "+name)
        df = combine_weather_order_traffic(df,needed_map_dir,name)
        df = add_poi(needed_map_dir,df,name)
    return df



def combine_weather_order_traffic(df,needed_map_dir,name):
    weather_path =  needed_map_dir+"/weather_data/weather_data_"+name
    traffic_path =  needed_map_dir+"/traffic_data/traffic_data_"+name
    order_path   =  needed_map_dir+"/order_data/order_data_"+name

    weather_data = pd.read_csv(weather_path)
    weather_data["Time"] = weather_data['date'].str.cat("-"+weather_data['time_slices'].astype(str))
    del weather_data["date"]
    del weather_data["week"]    
    del weather_data['time_slices']
    traffic_data = pd.read_csv(traffic_path)
    del traffic_data["date"]
    del traffic_data["week"]  
    order_data = pd.read_csv(order_path)


    df = pd.merge(order_data,traffic_data,left_on=["Time","start_district"],right_on=["Time","district"],how="right")
    
    df = pd.merge(df,weather_data,on=["Time"],how="left")
    df.set_index(["Time","start_district"])

    directory = needed_map_dir+"/feature_data_final"
    file_name = needed_map_dir+"/feature_data_final/feature_data_final_"+name
    if not os.path.exists(directory):
        os.makedirs(directory)

    #df.to_csv(file_name, index=False)
    df.set_index(['start_district','Time'])
    del df["Unnamed: 0"]
    return df

def add_poi(needed_map_dir,df,name):
    save = os.path.join(UPSET_DIR,CONCRETE_DIR,POI_SHEET_DIR)
    data = pd.read_csv(save+"/poi_features.csv")
  
    df = pd.merge(df.reset_index(["Time","start_district"]),data,left_on=["start_district"],right_on=["district"],how="left")
    file_name = needed_map_dir+"/feature_data_final/feature_data_final_"+name
    #del df["Unnamed: 0"]
    df.to_csv(file_name,index=False)
    return df


if __name__ == '__main__':
    needed_map_dir = os.path.join(UPSET_DIR, CONCRETE_DIR)
    #combine_weather_order_traffic(needed_map_dir)
 
    df = combine_all_dir(needed_map_dir)
    #print(df.head())
  
    print(df)