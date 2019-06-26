#! /usr/bin/python3
# coding : utf-8
"""
Created on Thu Mar 20 10:31:33 2019

@author: wyatt

This script can load some dat data and then draw time-resolved images.
这个脚本可以加载一些dat的数据，然后画出时间分辨图像。
这个脚本主要是画位置3(激射)数据移动delay
"""

from wyatt_function import load_dat_data, plot_time_image, get_xmin_xmax
import matplotlib.pyplot as plt


def main():
    folder = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\Tm_quantum dots1\800+400double_pulse"
    # file1 = r"\3\800shuang guang zi\alter\13-8.dat"  # 只有相同功率的红光
    file1 = r"\3\400+800 13.8mw\alter\0.dat"  # 只有相同功率的紫光
    file2 = r"\3\400+800 13.8mw\alter\8.dat"  # 两束光同时打上的数据,但时间上差的比较多，用来排除加热效应
    file3 = r"\3\400+800 13.8mw\alter\3.dat"  # 两束光同时打上的数据,但时间上差的比较多，用来排除加热效应
    file4 = r"\3\400+800 13.8mw\alter\9-5.dat"  # 两束光同时打上的数据
    ### 1.加载理论上的数据
    real_data1 = load_dat_data(folder + file1)  # 只有相同功率的紫光的数据
    real_data2 = load_dat_data(folder + file2)  # 两束光都打上的数据
    
    ### 2.构建理论的数据
    # 移动红光位置
    # red_move_data = move_data_time(red_excition_data)
    # theory_data1 = theory_data_construct(delay_data, red_move_data)
    # 移动紫光位置
    # real_data1 = move_data_time(real_data1, cur_pos=61, pur_pos=40)
    # theory_data = theory_data1
    
    ### 3.获取实际数据
    real_data3 = load_dat_data(folder + file3)
    # real_data3 = move_data_time(real_data3, cur_pos=15, pur_pos=25)
    real_data4 = load_dat_data(folder + file4)
    
    ### 4.画图
    plot_data(real_data1, real_data2, real_data3, real_data4)


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
    
    plt.figure(figsize=(8, 6))
    
    xmin, xmax = get_xmin_xmax(data1)
    plot_time_image(data1, xmin, xmax, l_label="delay:60ps", style="r-")
    
    if len(data2) > 1:
        xmin, xmax = get_xmin_xmax(data2)
        #plot_time_image(data2, xmin, xmax, l_label="delay:11ps", style="b-")
    
    if len(data3) > 1:
        xmin, xmax = get_xmin_xmax(data3)
        plot_time_image(data3, xmin, xmax, l_label="delay:43ps",  style="b-")
    
    if len(data4) > 1:
        xmin, xmax = get_xmin_xmax(data4)
        plot_time_image(data4, xmin, xmax, l_label="delay:-5ps", style="g-")
    plt.title("400nm 2.24mW and 800nm 13.8mW")
    plt.show()
    
    

if __name__ == '__main__':
    main()

