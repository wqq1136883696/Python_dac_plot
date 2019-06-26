#! /usr/bin/python3
# coding : utf-8

"""
Created on Monday Apr 1 15:01:17 2019

@author: wyatt

The purpose of the script is save my function.
time = get_lifetime(times, data)  获得寿命大小
    
min_position, max_position = get_xmin_xmax(data, range=0.5)  
获取x的取值范围

min_position, max_position = get_ymin_ymax(data, range=0.5)  
获取y的取值范围

move_data = move_data_time(ori_data, cur_pos=166, pur_pos=130) 移动数据到想要的位置

plot_spec_image(data, x_min, x_max)  画出光谱图像

plot_time_image(data, y_min, y_max)  画出寿命图像

yvals = polyfit(x, y, number=1)  多项式拟合

time, wavelength, max_data = read_max_data(ori_data)  
获取最大值对应的时间，获取最大值对应的波长，获取最大值

show_image(data)  显示图片

ori_data = subtract_background(ori_data, stu=1, extend=190) 减去数据背景
"""

import numpy as np
import matplotlib.pyplot as plt


def get_lifetime(times, data):
    """
        获得寿命大小
        Input parameter:
            (画时间分辨图的数据)
            times为时间列表
            data为对原有数据进行截取后求和标准化的数据，和times为一样的长度
        Output parameter：
            寿命大小
    """
    start_position = data.argmax()
    start_time = times[start_position]    # 获得最大值位置的时间
    std_data = data / data.max()    # 把数据进行归一化
    
    # 获得1/e位置的时间
    if std_data[-1] > (1 / np.e):
        return 80
    else:
        data_part = std_data[start_position:]
        end_portion = start_position + np.argmin(np.abs(data_part - (1 / np.e)))
        end_time = times[end_portion]
        return end_time - start_time


def get_xmin_xmax(data, r=0.5, statu=1):
    """
        获取x的取值范围
        算法：对每列求和，取出大于第一个最大值的一定比例的位置，作为最小的位置
            取小于最大值一定比例的位置，作为最大的位置
        Input parameter:
            data为原始数据，包括第一行波长和第一列时间
            r为range，range=0.5,为选取的数据范围，可以是(0:1),range越大，选取的数据越少
            statu为数据状态，1为原始数据,0为去掉坐标轴的位置
        Output parameter：
            min_position最小值的位置
            max_position最大值的位置
    """
    min_position = 0
    max_position = 0
    
    if statu:
        whole_img_data = data[1:, 1:]
    else:
        whole_img_data = data
    x_data = whole_img_data.sum(0)
    x_data = x_data / np.max(x_data)

    # 获取最小值
    min_x_position_list = np.where(x_data > r)
    for i in range(np.size(min_x_position_list[0])):
        if (min_x_position_list[0][i + 1] - min_x_position_list[0][i] == 1
                and min_x_position_list[0][i + 2] - min_x_position_list[0][i + 1] == 1):
            min_position = min_x_position_list[0][i]
#            print(min_position)
            break

    # 获得最大值的位置
    max_x_position_list = np.where(x_data[min_position:] < r)
    for j in range(np.size(max_x_position_list[0])):
        if (max_x_position_list[0][j + 1] - max_x_position_list[0][j] == 1
                and max_x_position_list[0][j + 2] - max_x_position_list[0][j + 1] == 1):
            max_position = max_x_position_list[0][j] + min_position
#            print(max_position)
            break
    return min_position, max_position


def get_ymin_ymax(data, r=0.4, statu=1):
    """获取y的取值范围
        算法：对每列求和，取出大于第一个最大值的一定比例的位置，作为最小的位置
            取小于最大值一定比例的位置，作为最大的位置
        Input parameter:
            data为原始数据，包括第一行波长和第一列时间
            r为range，range=0.5,为选取的数据范围，可以是(0:1),range越大，选取的数据越少
        Output parameter：
            min_position最小值的位置
            max_position最大值的位置
    """
    min_position = 0
    max_position = 0
    
    if statu:
        whole_img_data = data[1:, 1:]
    else:
        whole_img_data = data

    y_data = whole_img_data.sum(1)
    y_data = y_data / np.max(y_data)

    # 获取最小值
    min_y_position_list = np.where(y_data > r)

    for i in np.arange(np.size(min_y_position_list[0])):
        if (min_y_position_list[0][i + 1] - min_y_position_list[0][i] == 1
                and min_y_position_list[0][i + 2] - min_y_position_list[0][i + 1] == 1):
            min_position = min_y_position_list[0][i]
#            print(min_position)
            break

    # 获得最大值的位置
    max_y_position_list = np.where(y_data[min_position:] < r)
    
    if np.size(max_y_position_list[0]) >= 3:
        for j in np.arange(np.size(max_y_position_list[0])):
            if (max_y_position_list[0][j + 1] - max_y_position_list[0][j] == 1
                    and max_y_position_list[0][j + 2] - max_y_position_list[0][j + 1] == 1):
                max_position = max_y_position_list[0][j] + min_position
    #            print(max_position)
                break
    
    if max_position == 0:
        max_position = -1
        
    return min_position, max_position


def move_data_time(ori_data, cur_pos=166, pur_pos=130):
    """
        对原始的数据进行移动
    :param ori_data: 原始的数据
    :param cur_pos: 当前位置
    :param pur_pos: 目标位置
    :return:移动后的数据
    """

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


def plot_spec_image(data, y_min, y_max):
    """
        画出光谱图像
        Input parameter:
            data为原始数据，为矩阵，第一行和第一列分别为波长和时间
            y_min, y_max,为调用函数get_ymin_ymax分析后的结果
        
    """
    image_data = data[y_min:y_max, 1:]
    print(image_data.shape)
    plt.subplot(121)
    plt.imshow(image_data, cmap=plt.cm.jet)

    plt.subplot(122)
    Y = image_data.sum(0)
    Y = Y / np.max(Y)
    X = data[0, 1:]
    center_wavelength = X[Y.argmax()]
    plt.plot(X, Y, label="%.1f nm" % center_wavelength)
    plt.legend()
    
    
def plot_time_image(data, x_min, x_max, l_label=None, style='-'):
    """
        画出寿命图像
        Input parameter:
            data为原始数据，为矩阵，第一行和第一列分别为波长和时间
            x_min, x_max,为调用函数get_xmin_xmax分析后的结果
    """
    image_data = data[1:, x_min:x_max]
    rows, cols = image_data.shape
    # plt.figure('lifetime')
    # plt.figure(figsize=(10, 5))
    # plt.subplot(121)
    # plt.imshow(image_data, cmap=plt.cm.jet)

    # plt.subplot(111)
    Y = image_data.sum(1) / cols
    #Y = Y / np.max(Y)
    X = data[1:, 0]
    # 计算寿命
    #lifetime = get_lifetime(X, Y)
    # plt.plot(X, Y, label=l_label + "  Lifetime: %.2f ps" % lifetime)
    plt.plot(X, Y, style, linewidth=3)
    # plt.xlim(0, 190)
    plt.xlim(40, 48)
    plt.ylim(10000, 20000)
    # plt.ylim(0, max(Y)*1.01)
    plt.xlabel('Time (ps)')
    plt.ylabel('PL Intensity')
    # plt.legend()
    return X, Y
    

def polyfit(x, y, number=1):
    """
        多项式曲线拟合
        Input parameter:
            x,y两个向量，number为拟合阶数，默认为1，为线性拟合
        Output parameter：
            yvals为拟合后对应的y数据
    """
    z1 = np.polyfit(x, y, number)  # 获得拟合系数
    p1 = np.poly1d(z1)  # 形成拟合函数
    print(p1)
    yvals = p1(x)  # 使用拟合函数求y的拟合值
    return yvals


def read_max_data(ori_data):
    """
        获取最大值对应的时间，获取最大值对应的波长，获取最大值
        Input parameter：
            ori_data为原始数据，为矩阵，第一行和第一列不是数据，分别为波长和时间
        Output parameter：
            time：最大值对应的时间
            wavelength：最大值对应的波长
            max_data：最大值
    """
    ori_data = np.double(ori_data)  # 数据类型转换
    data = ori_data[1:, 1:]
    
    arg_max = np.argmax(data)  # 获取最大值的位置
    row = arg_max // data.shape[1]  # 获取最大值所在的行
    col = arg_max % data.shape[1]  # # 获取最大值所在的列
    max_data = np.max(data)
    # max_data1 = data[row, col]
    
    time = ori_data[row+1, 0]  # 获取最大值对应的时间
    wavelength = ori_data[0, col+1]  # 获取最大值对应的波长
    return time, wavelength, max_data


def show_image(data):
    """
        显示图片
        Input parameter：
            data为包括第一行喝第一列的原始数据
    """
    image_data = data[1:, 1:]
#    image_data = image_data.astype(np.uint8)
    plt.imshow(image_data, cmap=plt.cm.jet)  # 显示图像，坐标位置
#    x = data[0, 1:]
#    y = data[1:, 0]
#    rows = x.shape[0]
#    cols = y.shape[0]
#    bounds = (x[-1], x[0], y[0], y[-1])
#    img.pcolor(x, y, image_data, rows, cols, bounds, 'NEAREST')
    plt.show()
    
    
def subtract_background(ori_data, stu=1, extend=190):
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