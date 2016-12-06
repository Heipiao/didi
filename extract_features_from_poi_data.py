#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-07 23:06:00
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
import numpy as np

## import local lib


DATA_DIR = "../season_1_sad/"

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"

POI_SHEET_DIR = "poi_data"


'''
it is obviously that poi data has: 25 first level category (1 ~ 25)
'''
## 


'''
feature one: the sum of secondary category sum in each main category
feature two: the number of missing secondary category in each main category
feature three: the number of rare secondary category in each main category
features four: the types of pois number each district have
'''
## for features four: three types of poi
Types_POI = OrderedDict()

rare_poi_secondary_categories = list()


def extract_each_main_secondary_category(each_district_poi):
    features = pd.Series()

    #print(each_district_poi)
    #print(each_district_poi["23_2"])
    #print(each_district_poi.index)

    ### variables for features one ### 
    ## --> sum of secondary category contained in mian category
    secondary_category_sum = 0
    feature_one_name = "secondary_category_sum"


    ### variables for features two ###
    ## --> how many secondary category main category missed
    no_secondary_category_count = 0
    feature_two_name = "secondary_category_missing_count"

    ### variables for features three
    ## --> rare secondary category number
    rare_secondary_category_count = 0
    feature_three_name = "rare_secondary_category_count"

    ### variables for features four
    poi_type_one_count = 0
    poi_type_two_count = 0
    poi_type_three_count = 0
    feature_four_name1 = "poi_type_one_count"
    feature_four_name2 = "poi_type_two_count"
    feature_four_name3 = "poi_type_three_count"

    previous_main_category = "1"
    for secondary_category in each_district_poi.index:
        #  print(secondary_category)
        if secondary_category == "district":
            features = features.append(pd.Series(each_district_poi[secondary_category], index = ["district"]))
            continue

        ## feature four
        if not each_district_poi[secondary_category] == 0:
            if secondary_category in Types_POI["type_one_pois"]:
                poi_type_one_count += 1
            if secondary_category in Types_POI["type_two_pois"]:
                poi_type_two_count += 1
            if secondary_category in Types_POI["type_three_pois"]:
                poi_type_three_count += 1


        now_mian_num = secondary_category.strip().split("_")[0]
        if previous_main_category == now_mian_num:
            
            ## feature one
            secondary_category_sum += each_district_poi[secondary_category]

            ## feature two:
            if each_district_poi[secondary_category] == 0:
                no_secondary_category_count += 1

            ## feature three:
            if not each_district_poi[secondary_category] == 0 \
                and secondary_category in rare_poi_secondary_categories:
                    rare_secondary_category_count += 1


        else:
            ## feature one
            # features = features.append(pd.Series(secondary_category_sum, 
            #                                     index = [previous_main_category + "_" + feature_one_name]))
            secondary_category_sum = each_district_poi[secondary_category]

            ## feature two:
            # features = features.append(pd.Series(no_secondary_category_count, 
            #                                     index = [previous_main_category + "_" + feature_two_name]))           
            if each_district_poi[secondary_category] == 0:
                no_secondary_category_count = 1
            ## feature three:
            # features = features.append(pd.Series(rare_secondary_category_count, 
            #                                     index = [previous_main_category + "_" + feature_three_name]))           

            if not each_district_poi[secondary_category] == 0 \
                and secondary_category in rare_poi_secondary_categories:
                    rare_secondary_category_count = 1

        previous_main_category = now_mian_num

    ## add the final main category sum into features
    ### add feature one with district 66
    # features = features.append(pd.Series(secondary_category_sum, 
    #                                             index = [previous_main_category + "_" + feature_one_name]))
    ### add feature two with district 66
    # features = features.append(pd.Series(no_secondary_category_count, 
    #                                         index = [previous_main_category + "_" + feature_two_name]))

    ### add feature three with district 66
    # features = features.append(pd.Series(rare_secondary_category_count, 
    #                                         index = [previous_main_category + "_" + feature_three_name]))

    ### add features four 
    features = features.append(pd.Series(poi_type_one_count, 
                                            index = [feature_four_name1]))
    features = features.append(pd.Series(poi_type_two_count, 
                                            index = [feature_four_name2]))
    features = features.append(pd.Series(poi_type_three_count, 
                                            index = [feature_four_name3]))

    return features


def get_rare_poi_secondary_category(poi_df):
    def add_rare_poi_secondary_category(x, rare_pois):
        if not x.name == "district":
            # if len(x[x == 0]) >= 40:
            #     rare_pois.append(x.name)
            rare_pois[x.name] = len(x[x == 0])
    #print("get the secondary_category poi which half of the diatrict do not have...")
    poi_secondary_categories_missing_district_count = OrderedDict()

    poi_df.apply(lambda x: add_rare_poi_secondary_category(x, poi_secondary_categories_missing_district_count), 
                axis = 0)

    #print(poi_secondary_categories_missing_district_count)

    for k, v in poi_secondary_categories_missing_district_count.items():
        if v >= 40:
            rare_poi_secondary_categories.append(k)

    #print(rare_poi_secondary_categories)
    return rare_poi_secondary_categories

def base_multi_typepoi(poi_df):

    Types_POI["type_one_pois"] = list()
    Types_POI["type_two_pois"] = list()
    Types_POI["type_three_pois"] = list()

    def get_poi_type(x):
        if not x.name == "district":
            if x.sum() < 900:

                Types_POI["type_one_pois"].append(x.name)
            elif x.sum() < 500000:

                Types_POI["type_two_pois"].append(x.name)
            else:

                Types_POI["type_three_pois"].append(x.name)

    poi_df.apply(lambda x: get_poi_type(x), axis = 0)

    # print(Types_POI["type_one_pois"])
    # print(Types_POI["type_three_pois"])

def extract_various_features(poi_df):
    ## things for createing features
    get_rare_poi_secondary_category(poi_df)
    base_multi_typepoi(poi_df)


    featured_poi_df = pd.DataFrame()
    featured_poi_df = poi_df.apply(extract_each_main_secondary_category, axis = 1)

    return featured_poi_df


def extract_features_for_poi(poi_dir):
    print("extracting featues from poi data: ", poi_dir)

    poi_data_df = pd.read_csv(os.path.join(poi_dir, "poi_data.csv"))

    featured_poi_df = extract_various_features(poi_data_df)
    return featured_poi_df

if __name__ == '__main__':
    pass
    # poi_data_df = pd.read_csv(os.path.join(DATA_DIR, CONCRETE_DIR, POI_SHEET_DIR,
    #                                         "poi_data.csv"))

    # # get_rare_poi_secondary_category(poi_data_df)
    # extract_various_features(poi_data_df)
    