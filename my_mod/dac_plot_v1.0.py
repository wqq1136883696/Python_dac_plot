#! /usr/bin/python3
# coding : utf-8

import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

fig = plt.figure("spec", figsize=(12, 8))
X_RANGE = 0.5   # 选取x轴（选择一定区间的波长）大于最大值的20%的数据
Y_RANGE = 0.5   # 选取y轴（选择一定区间的时间）大于最大值的20%的数据


# Windows平台
folder_path = "G:\Group_Work\Wyatt_Experiment\Quantum_dot\Tm_20190227\One\Dac"


# Linux平台


def show_file():
    """显示文件夹下的dac文件列表"""
    dac_list = []
    dirs = os.listdir(folder_path)

    for i in dirs:  # 循环读取路径下的文件并筛选输出
        if os.path.splitext(i)[1] == ".dac":  # 筛选dac文件
            dac_list.append(i)
    return dac_list


def load_file(file_name):
    """加载数据文件，保存到data中"""
    input_file_path = folder_path + "\\" + file_name
    # out_file_path = folder_path + "\\alter\\" + file_name.split('.')[0] + ".csv"
    out_file_path = folder_path + "\\alter\\" + file_name

    #  读取有多少行，多少列元素
    rows = 0
    cols = 0
    output_file = open(out_file_path, 'w')
    # writer = csv.writer(file_csv, delimiter='\t', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    with open(input_file_path, 'r') as input_f:
        for data in input_f:
            # 把第一行的ps|nm换成0，方便计算
            str_list = data.split("\t")
            cols = len(str_list)
            if rows == 0:
                data = "0" + "\t" + data[6:]

            output_file.writelines(data)
            rows += 1
    # 关闭输出文件
    output_file.close()

    # 把数据保存到data中
    row = 0
    data = np.ones([rows, cols])
    with open(out_file_path, 'r') as f:
        for line in f:
            str_list = line.split("\t")
            # print(str_list)
            data[row] = np.array(str_list)
            row += 1
    return data


def show_image(data):
    """显示图片"""

    image_data = data[1:, 1:]
    # mpimg.pcolor(X, Y, image_data,)
    plt.subplot(231)
    ax = plt.imshow(image_data, cmap=plt.cm.jet)  # 显示图像，坐标位位置


def time_image(data, y_min, y_max):
    """画出寿命图像"""
    image_data = data[1:, y_min:y_max]
    print(image_data.shape)
    # plt.figure('lifetime')
    plt.subplot(232)
    plt.imshow(image_data, cmap=plt.cm.jet)

    plt.subplot(233)
    Y = image_data.sum(1)
    X = data[1:, 0]
    lifetime = get_lifetime(X, Y)
    plt.plot(X, Y, label="%.2f ps" % lifetime)
    plt.legend()


def get_lifetime(times, data):
    """获得寿命大小"""
    start_time = times[data.argmax()]    # 获得最大值位置的时间
    std_data = data / data.max()    # 把数据进行归一化

    # 以字典的形式保存到文件
    save_dict = {"times": times.tolist(),
                 "std_data": std_data.tolist(),
                 "data": data.tolist()}
    with open(folder_path + "\\alter\\no_800.json", 'w') as f:
        json.dump(save_dict, f)

    # save_list = [times.tolist(), std_data.tolist(), data.tolist()]
    # name = ["time", "std_data", "data"]
    # save_data = pd.DataFrame(columns=name, data=save_list)
    # save_data.to_csv(folder_path + "\\alter\\no_800.csv")

    # 按行存储
    # with open(folder_path + "\\alter\\no_800.csv", 'w') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(times)
    #     writer.writerow(std_data)

    end_time = times[np.argmin(np.abs(std_data - (1 / np.e)))]  # 获得1/e位置的时间
    return end_time - start_time


def spec_image(data, x_min, x_max):
    """画出光谱图像"""
    image_data = data[x_min:x_max, 1:]
    print(image_data.shape)
    plt.subplot(234)
    plt.imshow(image_data, cmap=plt.cm.jet)

    plt.subplot(235)
    Y = image_data.sum(0)
    X = data[0, 1:]
    center_wavelength = X[Y.argmax()]
    plt.plot(X, Y, label="%.1f nm" % center_wavelength)
    plt.legend()


def get_xmin_xmax(data):
    """获取x的取值范围
        算法：对每列求和，取出大于第一个最大值的一定比例的位置，作为最小的位置
            取小于最大值一定比例的位置，作为最大的位置
    """
    min_position = 0
    max_position = 0

    whole_img_data = data[1:, 1:]
    x_data = whole_img_data.sum(0)

    # 获取最小值
    min_x_position_list = np.where(x_data > (x_data.max() * X_RANGE))
    for i in range(len(min_x_position_list[0])):
        if (min_x_position_list[0][i + 1] - min_x_position_list[0][i] == 1
                and min_x_position_list[0][i + 2] - min_x_position_list[0][i + 1] == 1):
            min_position = min_x_position_list[0][i]
            print(min_position)
            break

    # 获得最大值的位置
    max_x_position_list = np.where(x_data[min_position:] < (x_data.max() * X_RANGE))
    for j in range(len(max_x_position_list[0])):
        if (max_x_position_list[0][j + 1] - max_x_position_list[0][j] == 1
                and max_x_position_list[0][j + 2] - max_x_position_list[0][j + 1] == 1):
            max_position = max_x_position_list[0][j] + min_position
            print(max_position)
            break
    return min_position, max_position


def get_ymin_ymax(data):
    """获取x的取值范围
        算法：对每列求和，取出大于第一个最大值的一定比例的位置，作为最小的位置
            取小于最大值一定比例的位置，作为最大的位置
    """
    min_position = 0
    max_position = 0

    whole_img_data = data[1:, 1:]
    y_data = whole_img_data.sum(1)

    # 获取最小值
    min_x_position_list = np.where(y_data > (y_data.max() * X_RANGE))
    for i in range(len(min_x_position_list[0])):
        if (min_x_position_list[0][i + 1] - min_x_position_list[0][i] == 1
                and min_x_position_list[0][i + 2] - min_x_position_list[0][i + 1] == 1):
            min_position = min_x_position_list[0][i]
            print(min_position)
            break

    # 获得最大值的位置
    max_x_position_list = np.where(y_data[min_position:] < (y_data.max() * X_RANGE))
    for j in range(len(max_x_position_list[0])):
        if (max_x_position_list[0][j + 1] - max_x_position_list[0][j] == 1
                and max_x_position_list[0][j + 2] - max_x_position_list[0][j + 1] == 1):
            max_position = max_x_position_list[0][j] + min_position
            print(max_position)
            break
    return min_position, max_position


def main():
    """主程序"""
    # 1.显示文件夹下的文件列表
    file_lists = show_file()
    print(file_lists)
    # 获取选定文件的内容
    plot_data(file_lists[0])


def plot_data(filename):
    """把选择的文件画图显示"""

    # 加载
    img_data = load_file(filename)
    show_image(img_data)
    x_min_position, x_max_position = get_xmin_xmax(img_data)
    time_image(img_data, x_min_position, x_max_position)
    y_min_position, y_max_position = get_ymin_ymax(img_data)
    spec_image(img_data, y_min_position, y_max_position)
    # print(xmin_position, xmax_position)

    plt.show()


if __name__ == '__main__':
    main()
