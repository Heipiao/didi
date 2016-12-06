#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-23 07:07:48
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
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

## import local lib

# import matplotlib
# matplotlib.use('MacOSX')

DATA_DIR = "../season_1_sad/" # only change this dir to change the operate dir

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"


TRAFFIC_SHEET_DIR = "traffic_data"

traffic_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR)

'''
b---blue   c---cyan  g---green    k----black
m---magenta r---red  w---white    y----yellow
'''

colors = dict()
colors["tj_l1_count"] = "r"
colors["tj_l2_count"] = "b"
colors["tj_l3_count"] = "g"
colors["tj_l4_count"] = "k"
# filled_markers = ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd')
markers_scatter = dict()
markers_scatter["tj_l1_count"] = "o"
markers_scatter["tj_l2_count"] = "^"
markers_scatter["tj_l3_count"] = "x"
markers_scatter["tj_l4_count"] = "."

line_style = dict()
# line_style["tj_l1_count"] = "-"
# line_style["tj_l2_count"] = "-."
# line_style["tj_l3_count"] = "--"
# line_style["tj_l4_count"] = ":"


line_style["tj_l1_count"] = "-"
line_style["tj_l2_count"] = "-"
line_style["tj_l3_count"] = "-"
line_style["tj_l4_count"] = "-"



# tj_level1_count  tj_level2_count  tj_level3_count tj_level4_count
# week  date  time  district
# Axes3D.scatter(xs, ys, zs=0, zdir='z', s=20, c='b', *args, **kwargs)
def plot_single_day_traffic(df):
    y_tj_l1 = df["tj_level1_count"]
    y_tj_l2 = df["tj_level2_count"]
    y_tj_l3 = df["tj_level3_count"]
    y_tj_l4 = df["tj_level4_count"]

    x_time = df["time_slices"]
    x_district = df["district"]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_time, x_district, y_tj_l1)
    # ax.plot_surface(x_time, x_district, y_tj_l1)
    print(plt.get_backend())
    #plt.show()
    plt.savefig("plot_traffic.png")
    

def plot_single_day_district_traffic(df, district_num, save_dir):
    single_district = df[df.district == district_num]

    fig = plt.figure()
    # show tj_level1_count 
    tj1_y = single_district["tj_level1_count"]
    time_x = single_district["time_slices"]
    tj1_p = fig.add_subplot(411)
    tj1_p.set_title("date: " + str(single_district.date.unique()[0]) +"," + " district: " + str(district_num))
    tj1_p.axis([0, 145, 0, max(tj1_y) + 50])
    tj1_p.set_ylabel("tj_level1_count")
    tj1_p.scatter(time_x, tj1_y)


    # show tj_level1_count 
    tj2_y = single_district["tj_level2_count"]
    time_x = single_district["time_slices"]
    tj2_p = fig.add_subplot(412)
    tj2_p.axis([0, 145, 0, max(tj2_y) + 50])
    tj2_p.set_ylabel("tj_level2_count")
    tj2_p.scatter(time_x, tj2_y)

    # show tj_level1_count 
    tj3_y = single_district["tj_level3_count"]
    time_x = single_district["time_slices"]
    tj3_p = fig.add_subplot(413)
    tj3_p.axis([0, 145, 0, max(tj3_y) + 50])
    tj3_p.set_ylabel("tj_level3_count")
    tj3_p.scatter(time_x, tj3_y)

    # show tj_level1_count 
    tj4_y = single_district["tj_level4_count"]
    time_x = single_district["time_slices"]
    tj4_p = fig.add_subplot(414)
    tj4_p.axis([0, 145, 0, max(tj4_y) + 50])
    tj4_p.set_ylabel("tj_level4_count")
    tj4_p.set_xlabel("time slice")
    tj4_p.scatter(time_x, tj4_y)
    
    save_file_name = "district: "+ str(district_num) + ".png"
    plt.savefig(os.path.join(save_dir, save_file_name))
    plt.close()

def traffic_level_this_district(df, d):
    splited_df = df.groupby(by = ["district", "time_slices"])
    time_slices_level1_count = -1 * np.ones((144,))
    time_slices_level2_count = -1 * np.ones((144,))
    time_slices_level3_count = -1 * np.ones((144,))
    time_slices_level4_count = -1 * np.ones((144,))

    for (dis, time), group in splited_df:
        if d == dis:
            time_slices_level1_count[time - 1] = group.tj_level1_count
            time_slices_level2_count[time - 1] = group.tj_level2_count
            time_slices_level3_count[time - 1] = group.tj_level3_count
            time_slices_level4_count[time - 1] = group.tj_level4_count
    tf_levels_count_time_slices = OrderedDict()
    tf_levels_count_time_slices["tj_l1_count"] = time_slices_level1_count
    tf_levels_count_time_slices["tj_l2_count"] = time_slices_level2_count
    tf_levels_count_time_slices["tj_l3_count"] = time_slices_level3_count
    tf_levels_count_time_slices["tj_l4_count"] = time_slices_level4_count
    return tf_levels_count_time_slices


def plot_single_day_district_traffic_all_level(df, district_num, save_dir):
    tf_levels_count_time_slices = traffic_level_this_district(df, district_num)
    time_s = range(1, 145)
    xmajorLocator = MultipleLocator(6) #将x主刻度标签设置为6的倍数
    xminorLocator = MultipleLocator(3) #将x轴次刻度标签设置为3的倍数

    for tf_key in tf_levels_count_time_slices.keys():
        #plt.scatter(x, y, s, c, marker, cmap, norm, vmin, vmax, alpha, linewidths, verts, edgecolors, hold, **data)
        plt.plot(time_s, tf_levels_count_time_slices[tf_key], 
                    label = tf_key, linestyle = line_style[tf_key], 
                    c = colors[tf_key], marker = markers_scatter[tf_key])
        ax = plt.gca()
        ax.set_title("district: " + str(district_num) + "  traffic level count")
            
        ax.legend(prop={'size':6})
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.xaxis.set_minor_locator(xminorLocator)
        ax.xaxis.grid(True, which='minor') #x坐标轴的网格使用主刻度
        #ax.xaxis.set_tick_params(length = 15)

        ax.set_xlim(0, 144)
        ax.set_ylim(bottom = -2)
        ax.set_xlabel("time slices")
        ax.set_ylabel("level count")

    save_file_name = "district: "+ str(district_num) + ".png"
    plt.savefig(os.path.join(save_dir, save_file_name))
    plt.close()

def plot_traffic_level_date_district():

    plot_saved_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR, 
                        "plot_traffic")
    if not os.path.exists(plot_saved_dir):
        os.mkdir(plot_saved_dir)

    #### Please Note: change this detail`s name when drawing different
    ## for : plot_single_day_district_traffic(..)
    #detail = "plot_traffic_level_date_district"
    ## for : plot_single_day_district_traffic_all_level(..)
    detail = "plot_traffic_all_levels_date_district"
    save_plot_dir = os.path.join(plot_saved_dir, detail)

    if not os.path.exists(save_plot_dir):
        os.mkdir(save_plot_dir)
    print("plotting: ", traffic_dir)
    if not os.path.isdir(traffic_dir) or not os.path.exists(traffic_dir):
        raise IOError("Not a dir or not existed")
    for file in sorted(os.listdir(traffic_dir)):
        if ".csv" in file:
            file_path = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR, file)
            df = pd.read_csv(file_path)
            current_date = str(df["date"].unique()[0])
            current_date_plot_dir = os.path.join(save_plot_dir, current_date)
            if not os.path.exists(current_date_plot_dir):
                os.mkdir(current_date_plot_dir)
            for dis_num in df.district.unique():
                #plot_single_day_district_traffic(df, dis_num, current_date_plot_dir)
                plot_single_day_district_traffic_all_level(df, dis_num, current_date_plot_dir)



















Monday = ["04", "11", "18"]
Tuesday = ["05", "12", "19", "26"]
Wednesday = ["06", "13", "20"]
Thursday = ["07", "14", "21", "28"]
Friday = ["08", "15", "22"]
Saturday = ["09", "16", "30"]
Sunday = ["10", "17", "24"]
Holiday = ["01", "02", "03"]

WEEKENDS = OrderedDict()
WEEKENDS["Monday"] = Monday
WEEKENDS["Tuesday"] = Tuesday
WEEKENDS["Wednesday"] = Wednesday
WEEKENDS["Thursday"] = Thursday
WEEKENDS["Friday"] = Friday
WEEKENDS["Saturday"] = Saturday
WEEKENDS["Sunday"] = Sunday
WEEKENDS["Holiday"] = Holiday

WEEK_colors = dict()
WEEK_colors[1] = "r"
WEEK_colors[2] = "b"
WEEK_colors[3] = "g"
WEEK_colors[4] = "k"
WEEK_markers_scatter = dict()
WEEK_markers_scatter[1] = "o"
WEEK_markers_scatter[2] = "^"
WEEK_markers_scatter[3] = "x"
WEEK_markers_scatter[4] = "."
WEEK_line_style = dict()
WEEK_line_style[1] = "--"
WEEK_line_style[2] = "--"
WEEK_line_style[3] = "--"
WEEK_line_style[4] = "--"

def count_has_data_number(dir, week_day):
    num = 0
    for f in os.listdir(dir):
        if ".csv" in f and f.strip().split("-")[-1][:2] in WEEKENDS[week_day]:
            num += 1
    return num

def plot_traffic_level_week_district(order_data_dir):
    plot_saved_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR, 
                            "plot_traffic")
    if not os.path.exists(plot_saved_dir):
        os.mkdir(plot_saved_dir)

    detail = "plot_traffic_week_district"
    save_plot_dir = os.path.join(plot_saved_dir, detail)
    if not os.path.exists(save_plot_dir):
        os.mkdir(save_plot_dir)

    time_s = range(1, 145)
    xmajorLocator = MultipleLocator(6) #将x主刻度标签设置为6的倍数
    xminorLocator = MultipleLocator(3) #将x轴次刻度标签设置为3的倍数

    for week_day in WEEKENDS.keys():
        print("plotting weekend: ", week_day)
        for d in range(1, 67):
            plot_portrait_flag = 0
            print("district: ", d)

            plot_week_date_num = 0
            for f in sorted(os.listdir(order_data_dir)):
                if ".csv" in f and f.strip().split("-")[-1][:2] in WEEKENDS[week_day]:

                    df = pd.read_csv(os.path.join(order_data_dir, f))
                    tf_levels_count_time_slices = traffic_level_this_district(df, d)

                    date_saved_dir = os.path.join(save_plot_dir, week_day)
                    if not os.path.exists(date_saved_dir):
                        os.mkdir(date_saved_dir)

                    plot_week_date_num += 1
                    plot_tj_level_num = 0
                    for tf_key in tf_levels_count_time_slices.keys():

                        plot_tj_level_num += 1
                        plt.subplot(4, 1, plot_tj_level_num)
                        plt.plot(time_s, tf_levels_count_time_slices[tf_key], 
                                label = df.date.unique()[0], linestyle = WEEK_line_style[plot_week_date_num], 
                                c = WEEK_colors[plot_week_date_num], marker = WEEK_markers_scatter[plot_week_date_num],
                                markersize = 4.5, linewidth = 1.5)
                        ax = plt.gca()

                        ax.set_ylabel("tj_l" + str(plot_tj_level_num) + " count")
                        if plot_week_date_num == 1 and plot_tj_level_num == 1:
                            ax.set_title("district: " + str(d) + "  traffic level count")

                        if plot_tj_level_num == 1:
                            ax.legend(prop={'size':5}, loc="lower right", shadow = False)

                        if plot_week_date_num == 1 and plot_tj_level_num == 4:
                            ax.set_xlabel("time slices")

                        ax.xaxis.set_major_locator(xmajorLocator)
                        ax.xaxis.set_minor_locator(xminorLocator)
                        ax.xaxis.grid(True, which='minor') #x坐标轴的网格使用主刻度
                        #ax.xaxis.set_tick_params(length = 15)

                        ax.set_xlim(0, 144)
                        ax.set_ylim(bottom = -2)


            try:        
                plt.savefig(os.path.join(date_saved_dir, "district_" + str(d) + ".png"))
                plt.close()
            except Exception:
                pass



DAYS_ONE = ["11", "12", "13", "14", "08", "09", "10"]
DAYS_TWO = ["18", "19", "20", "21", "15", "16", "17"]
DAYS_THREE = ["04", "05", "06", "07", "01", "02", "03"]
DAYS_FOUR = ["04", "05", "06", "07"]
DAYS_FIVE = ["01", "08", "15"]
DAYS_SIX = ["02", "09", "16"]
DAYS_SEVEN = ["03", "10", "17"]
DAYS_EIGHT = ["01", "02", "03", "09", "10", "16", "17"]

DAYS_STYLE = OrderedDict()
DAYS_STYLE["plot_whole_Week_one"] = DAYS_ONE
DAYS_STYLE["plot_whole_Week_two"] = DAYS_TWO
DAYS_STYLE["plot_whole_Week_three"] = DAYS_THREE
DAYS_STYLE["plot_working_days"] = DAYS_FOUR
DAYS_STYLE["plot_contain_holiady_friday"] = DAYS_FIVE
DAYS_STYLE["compare_holiady_saturday"] = DAYS_SIX
DAYS_STYLE["compare_holiady_sunday"] = DAYS_SEVEN
DAYS_STYLE["compare_holiady_day_off"] = DAYS_EIGHT

'''
b---blue   c---cyan  g---green    k----black
m---magenta r---red  w---white    y----yellow
'''
DAYS_colors = dict()
DAYS_colors[1] = "r"
DAYS_colors[2] = "b"
DAYS_colors[3] = "g"
DAYS_colors[4] = "k"
DAYS_colors[5] = "y"
DAYS_colors[6] = "c"
DAYS_colors[7] = "m"
# o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd'
DAYS_markers_scatter = dict()
DAYS_markers_scatter[1] = "o"
DAYS_markers_scatter[2] = "^"
DAYS_markers_scatter[3] = "x"
DAYS_markers_scatter[4] = "."
DAYS_markers_scatter[5] = "D"
DAYS_markers_scatter[6] = ">"
DAYS_markers_scatter[7] = "v"

DAYS_line_style = dict()
DAYS_line_style[1] = "--"
DAYS_line_style[2] = "--"
DAYS_line_style[3] = "--"
DAYS_line_style[4] = "--"
DAYS_line_style[5] = "--"
DAYS_line_style[6] = "--"
DAYS_line_style[7] = "--"

def plot_traffic_district_days(order_data_dir):
    plot_saved_dir = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR, 
                            "plot_traffic")
    if not os.path.exists(plot_saved_dir):
        os.mkdir(plot_saved_dir)

    detail = "plot_days_district_order"
    save_plot_dir = os.path.join(plot_saved_dir, detail)
    if not os.path.exists(save_plot_dir):
        os.mkdir(save_plot_dir)

    time_s = range(1, 145)
    xmajorLocator = MultipleLocator(6) #将x主刻度标签设置为6的倍数
    xminorLocator = MultipleLocator(3) #将x轴次刻度标签设置为3的倍数

    for days_style in DAYS_STYLE.keys():
        print("plotting days: ", days_style)
        for d in range(1, 67):
            plot_portrait_flag = 0
            print("district: ", d)

            plot_date_num = 0
            for f in sorted(os.listdir(order_data_dir)):
                if ".csv" in f and f.strip().split("-")[-1][:2] in DAYS_STYLE[days_style]:

                    df = pd.read_csv(os.path.join(order_data_dir, f))
                    tf_levels_count_time_slices = traffic_level_this_district(df, d)

                    date_saved_dir = os.path.join(save_plot_dir, days_style)
                    if not os.path.exists(date_saved_dir):
                        os.mkdir(date_saved_dir)

                    plot_date_num += 1
                    plot_tj_level_num = 0
                    for tf_key in tf_levels_count_time_slices.keys():

                        plot_tj_level_num += 1
                        plt.subplot(4, 1, plot_tj_level_num)
                        plt.plot(time_s, tf_levels_count_time_slices[tf_key], 
                                label = df.date.unique()[0], linestyle = DAYS_line_style[plot_date_num], 
                                c = DAYS_colors[plot_date_num], marker = DAYS_markers_scatter[plot_date_num],
                                markersize = 4.5, linewidth = 1.5)
                        ax = plt.gca()

                        ax.set_ylabel("tj_l" + str(plot_tj_level_num) + " count")
                        if plot_date_num == 1 and plot_tj_level_num == 1:
                            ax.set_title("district: " + str(d) + "  traffic level count")

                        if plot_tj_level_num == 1:
                            ax.legend(prop={'size':5}, loc="lower right", shadow = False)

                        if plot_date_num == 1 and plot_tj_level_num == 4:
                            ax.set_xlabel("time slices")

                        ax.xaxis.set_major_locator(xmajorLocator)
                        ax.xaxis.set_minor_locator(xminorLocator)
                        ax.xaxis.grid(True, which='minor') #x坐标轴的网格使用主刻度
                        #ax.xaxis.set_tick_params(length = 15)

                        ax.set_xlim(0, 144)
                        ax.set_ylim(bottom = -2)


            try:        
                plt.savefig(os.path.join(date_saved_dir, "district_" + str(d) + ".png"))
                plt.close()
            except Exception:
                pass





if __name__ == '__main__':
    file = "traffic_data_2016-01-20.csv"
    path = os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR, file)
    df = pd.read_csv(path)
    # print(df)
    # plot_single_day_traffic(df)
    # plot_single_day_district_traffic_all_level(df, 5, "./")
    plot_traffic_level_date_district()
    # plot_traffic_level_week_district(os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR))
    # plot_traffic_district_days(os.path.join(DATA_DIR, CONCRETE_DIR, TRAFFIC_SHEET_DIR))