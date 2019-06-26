# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 21:36:50 2019

@author: wyatt

This script is a time-resolved image of variable power.
这个脚本是画出变功率的时间分辨图像。(位置3)
"""

import numpy as np
import matplotlib.pyplot as plt
from wyatt_function import load_dat_data, plot_time_image, get_xmin_xmax
from wyatt_function import move_data_time, subtract_background

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
    

folder = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\Tm_quantum dots1\800+400double_pulse\weizhi5\400+800change 400power\alter"

# 改变400功率
file1 = r"\1-64.dat"
file2 = r"\1-387.dat"
file3 = r"\1-125.dat"
file4 = r"\0-857.dat"
file5 = r"\0-598.dat"

## 改变800功率
#file1 = r"\14-5.dat"
#file2 = r"\9-75.dat"
#file3 = r"\7-66.dat"
#file4 = r"\3-8.dat"
#file5 = r"\1-27.dat"



real_data1 = subtract_background(load_dat_data(folder + file1), extend=230)
real_data1 = move_data_time(real_data1, cur_pos=20, pur_pos=30)

real_data2 = subtract_background(load_dat_data(folder + file2), extend=230)
#real_data2 = move_data_time(real_data2, cur_pos=20, pur_pos=17)

real_data3 = subtract_background(load_dat_data(folder + file3), extend=230)
#real_data3 = move_data_time(real_data3, cur_pos=15, pur_pos=18)

real_data4 = subtract_background(load_dat_data(folder + file4))
#real_data4 = move_data_time(real_data4, cur_pos=15, pur_pos=18)

real_data5 = subtract_background(load_dat_data(folder + file5))


### 4.画图
plot_data(real_data1, real_data2, real_data3, real_data4,  real_data5)
plt.title('400nm + 800nm change 400nm power')

