#!/usr/bin/python
#-*- coding:utf-8 -*-

import time
import random
import sqlite3
import argparse
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from functools import wraps


parser = argparse.ArgumentParser()
parser.add_argument('-d', "--database", help="解析数据库文件名")
parser.add_argument('-s', "--startstamp", help="时间戳开始时间")
parser.add_argument('-e', "--endstamp", help="时间戳结束时间")
args = parser.parse_args()

sdkName = 'me.ele.lab.Example.EOTNormandy'
databaseName = args.database
startTime = args.startstamp
endTime = args.endstamp
batteryLeveltable = 'PLBatteryAgent_EventBackward_BatteryUI'
sdkNodeIdTable = 'PLAccountingOperator_EventNone_Nodes'

#数据库连接装饰器
def database_connector(a_fun):
    wraps(a_fun)
    def decorated(*args, **kwargs):
        conn = sqlite3.connect(databaseName)
        global c
        c = conn.cursor()
        return a_fun(*args, **kwargs)
        conn.commit()
        conn.close()
    return decorated

#时间戳转换为本地时间
def stramp_to_time(timestamp):
    timeArray = time.localtime(timestamp)
    localTime = time.strftime('%y-%m-%d %H:%M:%S', timeArray)
    localTime = localTime.split(' ')[1]
    return localTime

#打开数据库并获取对应表的所有数据
def select_table_data(tableName):
    c.execute("SELECT * FROM {form}".format(form=tableName))
    selectData = c.fetchall()
    return selectData

#生成图表文件
def draw_chart(*args):
    form_data = []
    for i in range(len(args)):
        if isinstance(args[i], list):
            form_data.append(args[i])
    x_data = form_data[0]; y_data = form_data[1:-1]; labelName = form_data[len(form_data)-1]
    lineColor_list = list(colors._colors_full_map.values())
    lineStyle_list = ['--', '-.', ':', '-']
    for i in range(len(y_data)):
        plt.plot(x_data, y_data[i], color=random.choice(lineColor_list), linestyle=random.choice(lineStyle_list))
    plt.title("sdk power usage")
    plt.legend(labelName); ax = plt.gca(); ax.spines['right'].set_color('none'); ax.spines['top'].set_color('none')
    plt.savefig('/Users/eleme/Desktop/power_usage.pdf')

#获取电量的使用百分比
@database_connector
def get_battery_level_usage(tableName, startStamp, endStamp):
    powerUsagelevel = []
    samplingPeriod = []
    data = select_table_data(tableName)
    for i in range(len(data)):
        if int(data[i][1]) in range(int(startStamp), int(endStamp)):
            samplingPeriod.append(stramp_to_time(data[i][1]))
            powerUsagelevel.append(data[i][3])
            powerUsagepercent = float(powerUsagelevel[0] - (powerUsagelevel[len(powerUsagelevel)-1]))
    draw_chart(samplingPeriod, powerUsagelevel, ['sdk usage percent'])
    return powerUsagepercent

#获取SDK的node id
@database_connector
def get__sdk_node_id(tabelName):
    data = select_table_data(tabelName)
    for i in range(len(data)):
        if str(data[i][3]) == sdkName:
            nodeId = data[i][0]
    return nodeId

if __name__ == '__main__':
    res1 = get_battery_level_usage(batteryLeveltable, startTime, endTime)
    res2 = get__sdk_node_id(sdkNodeIdTable)
    print res1, res2









