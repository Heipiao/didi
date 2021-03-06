#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-24 18:29:51
# @Author  : chensijia (2350543676@qq.com)
# @Version : 0.0.0
# @Style   : Python3.4
#
# @Description: 

## import python`s own lib
import os

## import third party lib
import pandas as pd
import matplotlib.pyplot as plt
## import local lib



DATA_DIR = "../season_1_sad/"

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"


WEATHER_SHEET_DIR = "weather_data"

def plot_single_day_weather(df, save_dir):
    y_pm = df["PM2.5"]
    y_wea = df["weather"]
    y_tem = df["temperature"] 

    x = df["time_slices"]  

    plt.figure(figsize=(8,7),dpi=98)
    
    # plt.title(str(df.date.unique()[0]) + "-day_weather")

    p_pm = plt.subplot(311)
    p_pm.set_title(str(df.date.unique()[0]) + "-day_weather")
    p_pm.set_ylabel("PM2.5")
    #p_pm.set_xlabel("time_slice")
    p_pm.grid(True)
    p_pm.axis([0, 150, 0, y_pm.max() + 5])
   
    p_wea = plt.subplot(312)
    p_wea.set_ylabel("weather")
    p_wea.axis([0, 150, 0, y_wea.max() + 1])
    #p_wea.set_xlabel("time_slice")
    p_wea.grid(True)

    p_tem = plt.subplot(313)
    p_tem.set_ylabel("tenperature")
    p_tem.set_xlabel("time_slice")
    p_tem.axis([0, 150, 0, y_tem.max() + 1])
    p_tem.grid(True)

    p_pm.plot(x, y_pm,"g-",label="PM2.5")
    p_wea.scatter(x, y_wea,label="weather_data",linewidth=2) 
    p_tem.plot(x, y_tem,"b.",label="temperature",linewidth=2)


    save_file_name = str(df.date.unique()[0]) + "-day_weather.png"
    plt.savefig(os.path.join(save_dir, save_file_name))
    plt.close()

def plot_weather():
    weather_dir = os.path.join(DATA_DIR, CONCRETE_DIR, WEATHER_SHEET_DIR)

    plot_dir = "plot_weather"
    current_date_plot_dir = os.path.join(DATA_DIR, CONCRETE_DIR, WEATHER_SHEET_DIR,\
                                         plot_dir)
    if not os.path.exists(current_date_plot_dir):
        os.mkdir(current_date_plot_dir)
    print("plotting: ", weather_dir)
    if not os.path.isdir(weather_dir) or not os.path.exists(weather_dir):
        raise IOError("Not a dir or not existed")
    for file in os.listdir(weather_dir):
        if ".csv" in file:
            file_path = os.path.join(DATA_DIR, CONCRETE_DIR, WEATHER_SHEET_DIR, file)
            df = pd.read_csv(file_path)
            plot_single_day_weather(df, current_date_plot_dir)



if __name__ == '__main__':
    plot_weather()