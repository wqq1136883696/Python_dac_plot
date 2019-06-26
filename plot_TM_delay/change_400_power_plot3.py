# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 21:36:50 2019

@author: wyatt

This script is a time-resolved image of variable power.
这个脚本是画出变功率的时间分辨图像。(位置3)
"""

import numpy as np
import matplotlib.pyplot as plt
from wyatt_function import load_dat_data, plot_time_image, get_xmin_xmax, move_data_time


def plot_data(data1, data2='0', data3='0', data4='0', data5='0'):
    # 画出理论上的图
    
    plt.figure(figsize=(12, 7))
    
    xmin, xmax = get_xmin_xmax(data1)
    plot_time_image(data1, xmin, xmax, l_label="13.7mW")
    
    if len(data2) > 1:
        xmin, xmax = get_xmin_xmax(data2)
        plot_time_image(data2, xmin, xmax, l_label="10.4mW")
    
    if len(data3) > 1:
        xmin, xmax = get_xmin_xmax(data3)
        plot_time_image(data3, xmin, xmax, l_label="7.52mW")
    
    if len(data4) > 1:
        xmin, xmax = get_xmin_xmax(data4)
        plot_time_image(data4, xmin, xmax, l_label="3.05mW")
        
    if len(data5) > 1:
        xmin, xmax = get_xmin_xmax(data5)
        plot_time_image(data5, xmin, xmax, l_label="0.93mW")
    
    plt.show()
    

folder = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\Tm_quantum dots1\800+400double_pulse\3\400+800change800power\alter"

## 改变400功率
# file1 = r"\3\800+400change400power\alter\2-41.dat"
# file2 = r"\3\800+400change400power\alter\2-11.dat"
# file3 = r"\3\800+400change400power\alter\1-69.dat"
# file4 = r"\3\800+400change400power\alter\1-28.dat"
# file5 = r"\3\800+400change400power\alter\0-56.dat"

file1 = r"\13-7.dat"
file2 = r"\10-4.dat"
file3 = r"\7-52.dat"
file4 = r"\3-05.dat"
file5 = r"\0-93.dat"



real_data1 = load_dat_data(folder + file1)
#real_data1 = move_data_time(real_data1, cur_pos=20, pur_pos=30)

real_data2 = load_dat_data(folder + file2)
#real_data2 = move_data_time(real_data2, cur_pos=20, pur_pos=17)

real_data3 = load_dat_data(folder + file3)
#real_data3 = move_data_time(real_data3, cur_pos=15, pur_pos=18)

real_data4 = load_dat_data(folder + file4)
#real_data4 = move_data_time(real_data4, cur_pos=15, pur_pos=18)

real_data5 = load_dat_data(folder + file5)


### 4.画图
plot_data(real_data1, real_data2, real_data3, real_data4,  real_data5)
plt.title('400nm + 800nm change 800nm power')

