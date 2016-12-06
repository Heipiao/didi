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

def features_order_dir(needed_map_dir):
    if not os.path.isdir(needed_map_dir) or not os.path.exists(needed_map_dir):
        raise IOError("ERROR: " + needed_map_dir + " not existed or its not a dir")
    print("order sheet... in " + needed_map_dir)
    for file in os.listdir(needed_map_dir):
        if ".csv" in file:
            file_path = os.path.join(needed_map_dir, file)
            print(file)
        
            # map all the district into concrete value
            data = pd.read_csv(file_path)
            data1 = data.drop_duplicates(["order_id"])
            data["NULL"] = data["driver_id"].isnull()
            grouped = data.groupby(["Time","start_district"])
            grouped1 = data1.groupby(["Time","start_district"])
            
            dd =  pd.Series()
            ddd =  pd.Series()

            for x in range(1,68):

            	ddd = ddd.append(dd)
            	dd =  pd.Series()
            	for y in range(1,145):
            		d = pd.Series(file[-14:-4]+"-"+str(y))
            		dd = dd.append(d)
            
            ss =  pd.Series()
            for s in range(1,67):
                for x in range(1,145):
                    ss = ss.append(pd.Series(s))
            
            # print(ddd.shape)
            # print(ss.shape)
            df = {"Time": pd.Series(ddd.values),
                  "start_district" : pd.Series(ss.values)}
            df = pd.DataFrame(df)

            df = passenger_base_feature(grouped,df)
            df = driver_base_feature(grouped,df)
            df = pd.merge(df,grouped.sum()["NULL"].astype(int).reset_index(["Time","start_district"]),on=["Time"  ,"start_district"],how="left")
            df = pd.merge(df,grouped.count()["dest_district"].reset_index(["Time","start_district"]),on=["Time"  ,"start_district"],how="left")
            df = df.rename(columns={"dest_district":"order_count"})
            df = pd.merge(df,pd.DataFrame(grouped.count()["order_id"]-grouped1.count()["order_id"]).reset_index(["Time","start_district"]),on=["Time"  ,"start_district"],how="left")
            df = df.rename(columns={"order_id":"null_1"})
            df["NULL"] = df["NULL"] +  df["null_1"] 
            #df["null_count"] = grouped.sum()["NULL"].astype(int)
            #df["order_count"] = grouped.count()["dest_district"]
            df.fillna(0,inplace=True)
            save_path = os.path.join(UPSET_DIR, CONCRETE_DIR,ORDER_SHEET_DIR,file)
            # change the file
            df.to_csv(save_path,index=True)
            print(df)
            #big_df = big_df.append(data)
   
    #df.to_csv("big_traffic.csv", index = True)

def passenger_base_feature(grouped,df):
    passenger_df_hash = pd.read_csv("passenger_df_hash.csv")
   
    dict_less_cab_take = dict(zip(passenger_df_hash.passenger_id,passenger_df_hash.less_cab_take))
    dict_high_cab_take = dict(zip(passenger_df_hash.passenger_id,passenger_df_hash.high_cab_take))
    random_cab_taker = dict(zip(passenger_df_hash.passenger_id,passenger_df_hash.random_cab_taker))
    coummter_cab_taker = dict(zip(passenger_df_hash.passenger_id,passenger_df_hash.coummter_cab_taker))

    many_start_taker = dict(zip(passenger_df_hash.passenger_id,passenger_df_hash.many_start_taker))
    less_start_taker = dict(zip(passenger_df_hash.passenger_id,passenger_df_hash.less_start_taker))
    many_dest_taker = dict(zip(passenger_df_hash.passenger_id,passenger_df_hash.many_dest_taker))
    less_dest_taker = dict(zip(passenger_df_hash.passenger_id,passenger_df_hash.less_dest_taker))

    d = pd.DataFrame(grouped.apply(lambda x: x.passenger_id.map(lambda x:dict_less_cab_take.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","passenger_num_less_cab_taker_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.passenger_id.map(lambda x:dict_high_cab_take.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","passenger_num_high_cab_taker_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.passenger_id.map(lambda x:random_cab_taker.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","passenger_num_random_cab_taker_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.passenger_id.map(lambda x:coummter_cab_taker.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","passenger_num_coummter_cab_taker_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.passenger_id.map(lambda x:many_start_taker.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","passenger_num_many_start_taker_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.passenger_id.map(lambda x:less_start_taker.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","passenger_num_less_start_taker_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.passenger_id.map(lambda x:many_dest_taker.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","passenger_num_many_dest_taker_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.passenger_id.map(lambda x:less_dest_taker.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","passenger_num_less_dest_taker_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")
    return df

 

    #df['passenger_mean_fee_cost'] = grouped.apply(lambda x: x.passenger_id.map(lambda x:less_dest_taker.get(x)).sum())

def driver_base_feature(grouped,df):
  
    driver_df_hash = pd.read_csv("driver_df_hash.csv")
    less_didi_use = dict(zip(driver_df_hash.driver_id,driver_df_hash.less_didi_use))
    more_didi_use = dict(zip(driver_df_hash.driver_id,driver_df_hash.more_didi_use))

    stable_loc_driver = dict(zip(driver_df_hash.driver_id,driver_df_hash.stable_loc_driver))
    random_loc_driver = dict(zip(driver_df_hash.driver_id,driver_df_hash.random_loc_driver))

    cheat_driver = dict(zip(driver_df_hash.driver_id,driver_df_hash.cheat_driver))

    d = pd.DataFrame(grouped.apply(lambda x: x.driver_id.map(lambda x:less_didi_use.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","driver_num_less_didi_use_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.driver_id.map(lambda x:more_didi_use.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","driver_num_more_didi_use_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.driver_id.map(lambda x:stable_loc_driver.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","driver_num_stable_loc_driver_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.driver_id.map(lambda x:random_loc_driver.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","driver_num_random_loc_driver_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")

    d = pd.DataFrame(grouped.apply(lambda x: x.driver_id.map(lambda x:cheat_driver.get(x,0)).sum()).reset_index(["Time"  ,"start_district"]))
    d.columns=["Time"  ,"start_district","driver_num_cheat_10"]
    df  = pd.merge(df,d,on=["Time"  ,"start_district"],how="left")
   
    return df

if __name__ == '__main__':
    path = os.path.join(DATA_DIR, CONCRETE_DIR,ORDER_SHEET_DIR)
    features_order_dir(path)

    