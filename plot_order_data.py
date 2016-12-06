#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-28 18:35:57
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


DATA_DIR = "../season_1_sad/"

TRAIN_FLAG = True
CONCRETE_DIR = "training_data" if TRAIN_FLAG else "test_set_1"


ORDER_SHEET_DIR = "order_data"

'''
b---blue   c---cyan  g---green    k----black
m---magenta r---red  w---white    y----yellow
'''

colors = dict()
colors[1] = "r"
colors[2] = "b"
colors[3] = "g"
colors[4] = "k"
# filled_markers = ('o', 'v', '^', '<', '>', '+', 'x', '8', 's', 'p', '*', 'h', 'H', 'D', 'd')
markers_scatter = dict()
markers_scatter[1] = "o"
markers_scatter[2] = "^"
markers_scatter[3] = "x"
markers_scatter[4] = "."

line_style = dict()
# line_style["tj_l1_count"] = "-"
# line_style["tj_l2_count"] = "-."
# line_style["tj_l3_count"] = "--"
# line_style["tj_l4_count"] = ":"


line_style[1] = "-"
line_style[2] = "-"
line_style[3] = "-"
line_style[4] = "-"

def plot_missed_time_slice(missed_sta):
    plot_saved_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR, 
                                    "plot_missed_time_slice")
    if not os.path.exists(plot_saved_dir):
        os.mkdir(plot_saved_dir)


    detail = "plot_district_slices"
    save_plot_dir = os.path.join(plot_saved_dir, detail)
    if not os.path.exists(save_plot_dir):
        os.mkdir(save_plot_dir)

    x = range(1, 67)
    xmajorLocator = MultipleLocator(10) #将x主刻度标签设置为10的倍数
    xmajorFormatter = FormatStrFormatter('%d') #设置x轴标签文本的格式 
    xminorLocator = MultipleLocator(5) #将x轴次刻度标签设置为1的倍数  
    for k, v in missed_sta.items():
        y = np.zeros(66)
        for missed_dis, missed_time_slices in v.items():
            y[missed_dis - 1] = len(missed_time_slices)

        plt.scatter(x, y)
        ax = plt.gca()
        ax.set_title("missed time slice statistic:")
        ax.set_xlabel("district")
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.xaxis.set_minor_locator(xminorLocator)
        ax.xaxis.set_minor_formatter(xmajorFormatter)
        ax.xaxis.grid(True, which='minor') #x坐标轴的网格使用次刻度
        ax.set_xlim(0, 66)
        ax.set_ylabel("missed time slices count")
        

        plt.savefig(os.path.join(save_plot_dir,  str(k) + ".png"))
        plt.close()


def plot_missed_time_slice_district(missed_sta):
    plot_saved_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR, 
                                "plot_missed_time_slice")
    if not os.path.exists(plot_saved_dir):
        os.mkdir(plot_saved_dir)

    detail = "plot_date_district"
    save_plot_dir = os.path.join(plot_saved_dir, detail)
    if not os.path.exists(save_plot_dir):
        os.mkdir(save_plot_dir)


    x = range(1, 22)
    xmajorLocator = MultipleLocator(1) #将x主刻度标签设置为10的倍数
    dates = list()
    for k, v in missed_sta.items():
        dates.append(k)
    print(dates)

    for i in range(1, 67):      
        y = list()
        for k in dates:
            if i in missed_sta[k].keys():
                y.append(len(missed_sta[k][i]))
            else:
                y.append(0)

        # print(len(y))
        plt.scatter(x, y)
        ax = plt.gca()
        ax.set_title("district: " + str(i) + " time slices missed ")
        ax.set_xlabel("date")
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
        ax.set_xlim(0, 22)
        #ax.set_xticklabels(dates)
        ax.set_ylabel("missed time slices count")
        
        plt.savefig(os.path.join(save_plot_dir, "district_" + str(i) + ".png"))
        plt.close()






def order_count_this_district(df, d):
    splited_df = df.groupby(by = ["start_district", "time_slices"])
    time_slices_order_count = -1 * np.ones((144,))
    for (dis, time), group in splited_df:
        if d == dis:
            time_slices_order_count[time - 1] = group.order_id.count()
    return time_slices_order_count

def plot_order_count_district_time_slices(order_data_dir):
    plot_saved_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR, 
                            "plot_orders_count")
    if not os.path.exists(plot_saved_dir):
        os.mkdir(plot_saved_dir)

    detail = "plot_district_slices_order"
    save_plot_dir = os.path.join(plot_saved_dir, detail)
    if not os.path.exists(save_plot_dir):
        os.mkdir(save_plot_dir)

    time_s = range(1, 145)
    xmajorLocator = MultipleLocator(6) #将x主刻度标签设置为6的倍数
    xminorLocator = MultipleLocator(3) #将x轴次刻度标签设置为3的倍数
    for f in os.listdir(order_data_dir):
        if ".csv" in f:
            df = pd.read_csv(os.path.join(order_data_dir, f))


            date_saved_dir = os.path.join(save_plot_dir, df.date.unique()[0])
            if not os.path.exists(date_saved_dir):
                os.mkdir(date_saved_dir)
            print("plotting: ", date_saved_dir)

            for d in df.start_district.unique():
                time_slices_order_count = order_count_this_district(df, d)
                plt.scatter(time_s, time_slices_order_count)
                ax = plt.gca()
                ax.set_title("district: " + str(d) + " time_slices order count ")


                ax.xaxis.set_major_locator(xmajorLocator)
                ax.xaxis.set_minor_locator(xminorLocator)
                ax.xaxis.grid(True, which='minor') #x坐标轴的网格使用主刻度
                #ax.xaxis.set_tick_params(length = 15)

                ax.set_xlim(0, 144)
                ax.set_ylim(bottom = -1.5)
                ax.set_xlabel("time slices")
                ax.set_ylabel("order count")
                
                plt.savefig(os.path.join(date_saved_dir, "district_" + str(d) + ".png"))
                plt.close()

def plot_order_count_date_district(order_data_dir):
    plot_saved_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR, 
                        "plot_orders_count")
    if not os.path.exists(plot_saved_dir):
        os.mkdir(plot_saved_dir)

    detail = "plot_date_district_order"
    save_plot_dir = os.path.join(plot_saved_dir, detail)
    if not os.path.exists(save_plot_dir):
        os.mkdir(save_plot_dir)

    time_s = range(1, 145)
    xmajorLocator = MultipleLocator(6) #将x主刻度标签设置为6的倍数
    xminorLocator = MultipleLocator(3) #将x轴次刻度标签设置为3的倍数

    for d in range(1, 67):
        plot_heng_flag = 0
        plot_shu_flag = 0
        print("plotting district: ", d)
        for f in sorted(os.listdir(order_data_dir)):
            if ".csv" in f:
                plot_heng_flag += 1
                df = pd.read_csv(os.path.join(order_data_dir, f))
                time_slices_order_count = order_count_this_district(df, d)

                plt.subplot(21, 1, plot_heng_flag)
                plt.scatter(time_s, time_slices_order_count)
                ax = plt.gca()

                
                ax.set_yticks([])
                #ax.set_ylim(bottom = -1.5, top = max(time_slices_order_count))
                ax.xaxis.set_major_locator(xmajorLocator)
                ax.xaxis.set_minor_locator(xminorLocator)
                ax.xaxis.grid(True, which='minor') #x坐标轴的网格使用主刻度
                ax.set_xlim(0, 144)
                #ax.set_xticks([])

                if plot_heng_flag == 1:
                    ax.set_title("district: " + str(d) + " time_slices order count ")
                if plot_heng_flag == 21:
                    ax.set_xlabel("time slices")
                    ax.set_ylabel("order count")


                    # ax.xaxis.grid(True, which='major') #x坐标轴的网格使用主刻度
                    #ax.xaxis.set_tick_params(length = 15)            
        plt.savefig(os.path.join(save_plot_dir, "district_" + str(d) + ".png"))
        plt.close()


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

def count_has_data_number(dir, week_day):
    num = 0
    for f in os.listdir(dir):
        if ".csv" in f and f.strip().split("-")[-1][:2] in WEEKENDS[week_day]:
            num += 1
    return num

def plot_order_count_district_week(order_data_dir):
    plot_saved_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR, 
                    "plot_orders_count")
    if not os.path.exists(plot_saved_dir):
        os.mkdir(plot_saved_dir)

    detail = "plot_week_district_order"
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
            plot_sub_num = count_has_data_number(order_data_dir, week_day)

            for f in sorted(os.listdir(order_data_dir)):
                if ".csv" in f and f.strip().split("-")[-1][:2] in WEEKENDS[week_day]:

                    df = pd.read_csv(os.path.join(order_data_dir, f))

                    date_saved_dir = os.path.join(save_plot_dir, week_day)
                    if not os.path.exists(date_saved_dir):
                        os.mkdir(date_saved_dir)

                    time_slices_order_count = order_count_this_district(df, d)

                    plot_portrait_flag += 1
                    plt.subplot(plot_sub_num, 1, plot_portrait_flag)
                    plt.scatter(time_s, time_slices_order_count, label = df.date.unique()[0])
                    ax = plt.gca()
                    if plot_portrait_flag < 2:
                        ax.set_title("district: " + str(d) + "  order count ")
                        
                    ax.legend(prop={'size':5})
                    ax.xaxis.set_major_locator(xmajorLocator)
                    ax.xaxis.set_minor_locator(xminorLocator)
                    ax.xaxis.grid(True, which='minor') #x坐标轴的网格使用主刻度
                    #ax.xaxis.set_tick_params(length = 15)

                    ax.set_xlim(0, 144)
                    ax.set_ylim(bottom = -1.5)
                    if plot_portrait_flag == plot_sub_num:
                        ax.set_xlabel("time slices")
                        ax.set_ylabel("order count")
            try:        
                plt.savefig(os.path.join(date_saved_dir, "district_" + str(d) + ".png"))
                plt.close()
            except Exception:
                pass

def plot_order_count_district_week_TWO(order_data_dir):
    plot_saved_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR, 
                    "plot_orders_count")
    if not os.path.exists(plot_saved_dir):
        os.mkdir(plot_saved_dir)

    detail = "plot_week_district_order_TWO"
    save_plot_dir = os.path.join(plot_saved_dir, detail)
    if not os.path.exists(save_plot_dir):
        os.mkdir(save_plot_dir)

    time_s = range(1, 145)
    xmajorLocator = MultipleLocator(6) #将x主刻度标签设置为6的倍数
    xminorLocator = MultipleLocator(3) #将x轴次刻度标签设置为3的倍数
    for week_day in WEEKENDS.keys():
        print("plotting weekend: ", week_day)
        for d in range(1, 67):
            print("district: ", d)
            plot_flag = 0
            for f in sorted(os.listdir(order_data_dir)):
                if ".csv" in f and f.strip().split("-")[-1][:2] in WEEKENDS[week_day]:

                    df = pd.read_csv(os.path.join(order_data_dir, f))

                    date_saved_dir = os.path.join(save_plot_dir, week_day)
                    if not os.path.exists(date_saved_dir):
                        os.mkdir(date_saved_dir)

                    time_slices_order_count = order_count_this_district(df, d)
                    plot_flag += 1
                    plt.plot(time_s, time_slices_order_count, 
                            label = df.date.unique()[0],linestyle = line_style[plot_flag], 
                            c = colors[plot_flag], marker = markers_scatter[plot_flag])
                    ax = plt.gca()
                    ax.set_title("district: " + str(d) + "  order count ")

                    ax.legend(prop={'size':5})
                    ax.xaxis.set_major_locator(xmajorLocator)
                    ax.xaxis.set_minor_locator(xminorLocator)
                    ax.xaxis.grid(True, which='minor') #x坐标轴的网格使用主刻度
                    #ax.xaxis.set_tick_params(length = 15)

                    ax.set_xlim(0, 144)
                    ax.set_ylim(bottom = -1.5)
                    ax.set_xlabel("time slices")
                    ax.set_ylabel("order count")
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


def plot_order_count_district_whole_week(order_data_dir):
    plot_saved_dir = os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR, 
                    "plot_orders_count")
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
        date_saved_dir = os.path.join(save_plot_dir, days_style)
        if not os.path.exists(date_saved_dir):
            os.mkdir(date_saved_dir)
        print("plotting days style: ", days_style)

        for d in range(1, 67):
            print("district: ", d)

            for day in DAYS_STYLE[days_style]:
                plot_portrait_flag = 0
                for f in sorted(os.listdir(order_data_dir)):
                    if ".csv" in f and f.strip().split("-")[-1][:2] == day:

                        df = pd.read_csv(os.path.join(order_data_dir, f))
                        time_slices_order_count = order_count_this_district(df, d)

                        #plot_portrait_flag += 1
                        #plt.subplot(7, 1, plot_portrait_flag)
                        plt.plot(time_s, time_slices_order_count, label = str(df.week.unique()[0]))
                        ax = plt.gca()
                        #if plot_portrait_flag < 2:
                        ax.set_title("district: " + str(d) + "  order count ")
                            
                        ax.legend(prop={'size':6})
                        ax.xaxis.set_major_locator(xmajorLocator)
                        ax.xaxis.set_minor_locator(xminorLocator)
                        ax.xaxis.grid(True, which='minor') #x坐标轴的网格使用次刻度
                        #ax.xaxis.set_tick_params(length = 15)

                        ax.set_xlim(0, 144)
                        ax.set_ylim(bottom = -1.5)
                        #if splited_df == 7:
                        ax.set_xlabel("time slices")
                        ax.set_ylabel("order count")
            try:        
                plt.savefig(os.path.join(date_saved_dir, "district_" + str(d) + ".png"))
                plt.close()
            except Exception:
                pass


if __name__ == '__main__':
    # plot_order_count_district_time_slices(os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR))
    # plot_order_count_date_district(os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR))
    plot_order_count_district_week(os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR))
    plot_order_count_district_week_TWO(os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR))
    #plot_order_count_district_whole_week(os.path.join(DATA_DIR, CONCRETE_DIR, ORDER_SHEET_DIR))