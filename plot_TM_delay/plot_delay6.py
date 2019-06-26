#! /usr/bin/python3
# coding : utf-8
"""
Created on Thu Mar 20 10:31:33 2019

@author: wyatt

This script can load some dat data and then draw time-resolved images.
这个脚本可以加载一些dat的数据，然后画出时间分辨图像。
这个脚本主要是画位置6(激射)数据移动delay
"""

from wyatt_function import load_dat_data, plot_time_image, get_xmin_xmax
import matplotlib.pyplot as plt
import numpy as np


def main():
    folder = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\Tm_quantum dots1\800+400double_pulse"
    
    # file1 = r"\weizhi6\400change400power\alter\2-46.dat"  # 只有相同功率的紫光
    file1 = r"\weizhi6\400+800change delay\alter\0.dat"
    file2 = r"\weizhi6\400+800change delay\alter\4.dat"  # 两束光同时打上的数据,但时间上差的比较多，用来排除加热效应
    file3 = r"\weizhi6\400+800change delay\alter\5-5.dat"  # 两束光同时打上的数据,但时间上差的比较多，用来排除加热效应
    file4 = r"\weizhi6\400+800change delay\alter\7.dat"  # 两束光同时打上的数据
    ### 1.加载理论上的数据
    real_data1 = subtract_background(load_dat_data(folder + file1))  # 只有相同功率的紫光的数据
    real_data2 = subtract_background(load_dat_data(folder + file2))  # 两束光都打上的数据
    
    ### 2.构建理论的数据
    # 移动红光位置
    # red_move_data = move_data_time(red_excition_data)
    # theory_data1 = theory_data_construct(delay_data, red_move_data)
    # 移动紫光位置
    real_data1 = move_data_time(real_data1, cur_pos=100, pur_pos=120)
    real_data2 = move_data_time(real_data2, cur_pos=130, pur_pos=120)
    # theory_data = theory_data1
    
    ### 3.获取实际数据
    real_data3 = subtract_background(load_dat_data(folder + file3))
    real_data3 = move_data_time(real_data3, cur_pos=15, pur_pos=25)
    
    real_data4 = subtract_background(load_dat_data(folder + file4))
    
    ### 4.画图
    plot_data(real_data1, real_data2, real_data3, real_data4)
    
    
def subtract_background(ori_data, stu=1, extend=0):
    """
    数据减去背景
    :param ori_data: 输入的数据
    :param stu: 状态默认为1，包含第一行喝第一列
    :param extend: 额外减去的部分
    :return: 返回减去背景的数据
    """
    if stu == 1:
        ori_data[1:, 1:] = ori_data[1:, 1:] - np.min(ori_data[1:, 1:]) - extend
    else:
        ori_data = ori_data - np.min(ori_data) - extend
    return ori_data
    

def move_data_time(ori_data, cur_pos=166, pur_pos=130):
    # 对原始的数据进行移动
    distance = cur_pos - pur_pos
    
    rows,cols = ori_data.shape
    # 构建移动后的数据
    move_data = ori_data
    
    if distance >= 0:  # 往前移动
        # 选取要移动的数据
        ori_part_data = ori_data[distance:, 1:]
        # 把选取出来的部分数据赋给move_data
        move_data[:rows-distance, 1:] = ori_part_data
    else:
        # 选取要移动的数据
        ori_part_data = ori_data[1: distance, 1:]
        # 把选取出来的部分数据赋给move_data
        move_data[-distance+1:, 1:] = ori_part_data
    return move_data


def theory_data_construct(ori_data, mod_data):
    # 构建理论上的数据
 
    # 先把原始数据赋给改变后的数据，主要想要第一行喝第一列的数据
    theory_data = ori_data
    
    # 把数据部分更新为修改后的额数据(把调制数据添加到原始数据上)
    theory_data[1:, 1:] = ori_data[1:, 1:] + mod_data[1:, 1:]
    return theory_data


def plot_data(data1, data2='0', data3='0', data4='0'):
    # 画出理论上的图
    
    plt.figure(figsize=(10, 5))
    
    xmin, xmax = get_xmin_xmax(data1)
    plot_time_image(data1, xmin, xmax, l_label="400nm 2.46mW and 800nm 14mW delay:45ps", style='b-')
    # plot_time_image(data1, xmin, xmax, l_label="400nm 1.6mW and 800nm 14mW delay:62ps")
    
    if len(data2) > 1:
        xmin, xmax = get_xmin_xmax(data2)
        plot_time_image(data2, xmin, xmax, l_label="400nm 2.46mW and 800nm 14mW delay:17ps")
    
    if len(data3) > 1:
        xmin, xmax = get_xmin_xmax(data3)
        plot_time_image(data3, xmin, xmax, l_label="400nm 2.46mW and 800nm 14mW delay:9ps", style='c-')
    
    if len(data4) > 1:
        xmin, xmax = get_xmin_xmax(data4)
        plot_time_image(data4, xmin, xmax, l_label="400nm 2.46mW and 800nm 14mW delay:-5ps", style='g--')
    
    plt.show()
    
    

if __name__ == '__main__':
    main()

