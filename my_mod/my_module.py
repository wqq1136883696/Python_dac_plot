#! /usr/bin/python3
# coding : utf-8

"""
Created on Friday Mar 22 21:34:17 2019

@author: wyatt

The purpose of the script is save my function.

Included Function：


"""

import os
import xlrd
import numpy as np
import matplotlib.pyplot as plt


class FileProcess(object):
    """
        这个类是包含一些对文件夹和文件的处理，包括文件的读取，保存

        data = load_dac_file(folder_path, file_name)
            加载第一次从条纹相机保存的dac数据文件，保存到data中

        data = load_dat_data(filename)  读取dat文件中的数据，转换成浮点矩阵

        sheet = load_xlsx(filename)  读取Excel表格

        loop_folder_dac2dat(pub_folder)  批量实现保存dac文件为dat文件

        list = show_file(folder_path, format='.dac')  显示文件夹下的dac文件列表

        folder_list= show_folder(folder_path)  显示folder_path下的文件夹列表
    """
    def __init__(self):
        pass

    @staticmethod
    def load_dac_file(pub_folder, file_name, sub_folder='dac'):
        """
            加载第一次从条纹相机保存的dac数据文件，保存到data中
            Input parameter:
                pub_folder为文件夹路径，字符串类型，不包括dac文件夹
                sub_folder为dac文件夹，值就是'dac'
                file_name为文件名，字符串类型
            Output parameter：
                data为文件中的数据，float类型
        """
        input_file_path = pub_folder + "\\" + sub_folder + "\\" + file_name
        out_file_path = pub_folder + "\\alter\\" + file_name.split('.dac')[0] + ".dat"

        #  读取有多少行，多少列元素
        rows = 0
        data = np.zeros((1017, 1345))
        with open(input_file_path, 'r') as input_f:
            for line in input_f:
                # 把第一行的ps|nm换成0，方便计算
                str_list = line.split("\t")
                if rows == 0:
                    str_list[0] = '0'

                data[rows, :] = str_list
                rows += 1

                if int(rows % 200) == 0:
                    print("执行第%d行" % rows)

        # 保存成python容易读取的数据文件，后缀为.dat
        np.savetxt(out_file_path, data, fmt='%s', delimiter='\t')
        data = data.astype(np.float32)  # 把字符串类型转换成float类型
        return data

    @staticmethod
    def load_dat_data(filename):
        """
            读取dat文件中的数据，转换成浮点矩阵
            Input parameter：
                filename为文件路径
        """
        data = np.loadtxt(filename)  # 加载文件数据，读取的为字符串
        data = data.astype(np.float32)  # 转换成浮点矩阵
        return data

    @staticmethod
    def load_xlsx(filename):
        """
            读取Excel表格
            Input parameter：
                filename为文件路径
            Output parameter：
                sheet为表格内容
        Example：
            1. 获取整行或者整列的值
                rows=sheet.row_values(2)#第三行内容
                cols=sheet.col_values(1)#第二列内容
            2. 获取单元格内容
                sheet.cell(1,0).value.encode('utf-8')
                sheet.cell_value(1,0).encode('utf-8')
                sheet.row(1)[0].value.encode('utf-8')

        """
        # 获取文件
        excel_file = xlrd.open_workbook(filename)

        # 读取sheet1
        sheet = excel_file.sheet_by_index(0)
        print(sheet.name, sheet.nrows, sheet.ncols)

        return sheet

    def loop_folder_dac2dat(self, pub_folder):
        """
            这个函数调用show_folder, show_file, load_dac_file,
            然后可以实现把pub_folder文件夹下的所有的dac文件夹中的dac文件转换成
            dat文件（以numpy数组的形式保存的，并且把第一行第一列的ps|nm换成0），
            可以使用np.loadtxt()直接读取

            采用的python递归的方法实现程序目标
        :param pub_folder: 文件夹路径
        :return:
        """
        folder_list = self.show_folder(pub_folder)
        if len(folder_list) > 0:  # 如果子文件夹存在，则循环显示子文件夹中的文件
            for folder in folder_list:

                if folder == 'dac':  # 如果文件夹为dac,则进行数据处理
                    dac_filename_list = self.show_file(pub_folder + "\\" + folder)  # 显示dac文件列表

                    if 'alter' in folder_list:  # 如果alter文件夹已经存在，显示dat列表
                        dat_filename_list = self.show_file(pub_folder + "\\alter", fmt='.dat')
                    else:  # 否则新建alter文件夹
                        os.mkdir(pub_folder + "\\alter")
                        dat_filename_list = []

                    if len(dat_filename_list) == 0:  # 如果列表为空，则进行数据保存
                        for filename in dac_filename_list:  # 进行保存数据的操作
                            self.load_dac_file(pub_folder, filename)

                self.loop_folder_dac2dat(pub_folder + "\\" + folder)  # 循环调用自身

    @staticmethod
    def show_file(folder_path, fmt='.dac'):
        """
            显示文件夹下的dac文件列表
            Input parameter:
                folder_path为文件夹路径，字符串类型
                format为所要查找的文件类型，默认为'.dac'
            Output parameter：
                list为当前文件夹下的满足格式的文件列表,是一个列表格式
        """
        list = []
        dirs = os.listdir(folder_path)

        for i in dirs:  # 循环读取路径下的文件并筛选输出
            if os.path.splitext(i)[1] == fmt:  # 默认筛选dac文件
                list.append(i)
        return list

    @staticmethod
    def show_folder(folder_path):
        """
            显示folder_path下的文件夹列表
        :param folder_path: 文件夹地址
        :return:folder_list：文件夹列表
        """
        folder_list = []
        dirs = os.listdir(folder_path)

        for file in dirs:  # 循环读取路径下的文件并筛选输出
            if len(file.split('.')) == 1:  # 筛选文件夹
                folder_list.append(file)
        return folder_list


class DataProcess(object):

    """
        数据处理模块

        time = get_lifetime(times, data)  获得寿命大小

        min_position, max_position = get_xmin_xmax()
        获取x的取值范围

        min_position, max_position = get_ymin_ymax()
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
    def __init__(self, data, x_range=0.5, y_range=0.5):
        self.data = data
        self.min_x_position = 0
        self.max_x_position = 0
        self.min_y_position = 0
        self.max_y_position = 0

        self.x_range = x_range
        self.y_range = y_range
        self.get_xmin_xmax()
        self.get_ymin_ymax()

    @staticmethod
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
        start_time = times[start_position]  # 获得最大值位置的时间
        std_data = data / data.max()  # 把数据进行归一化

        # 获得1/e位置的时间
        if std_data[-1] > (1 / np.e):
            return 80
        else:
            data_part = std_data[start_position:]
            end_portion = start_position + np.argmin(np.abs(data_part - (1 / np.e)))
            end_time = times[end_portion]
            return end_time - start_time

    def get_xmin_xmax(self):
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

        whole_img_data = self.data[1:, 1:]

        x_data = whole_img_data.sum(0)
        x_data = x_data / np.max(x_data)

        # 获取最小值
        min_x_position_list = np.where(x_data > self.x_range)
        for i in range(len(min_x_position_list[0])):
            if (min_x_position_list[0][i + 1] - min_x_position_list[0][i] == 1
                    and min_x_position_list[0][i + 2] - min_x_position_list[0][i + 1] == 1):
                self.min_x_position = min_x_position_list[0][i]
                break

        # 获得最大值的位置
        max_x_position_list = np.where(x_data[self.min_x_position:] < self.x_range)
        for j in range(len(max_x_position_list[0])):
            if (max_x_position_list[0][j + 1] - max_x_position_list[0][j] == 1
                    and max_x_position_list[0][j + 2] - max_x_position_list[0][j + 1] == 1):
                self.max_x_position = max_x_position_list[0][j] + self.min_x_position
                break

    def get_ymin_ymax(self):
        """获取y的取值范围
            算法：对每列求和，取出大于第一个最大值的一定比例的位置，作为最小的位置
                取小于最大值一定比例的位置，作为最大的位置
            Input parameter:
                data为原始数据，包括第一行波长和第一列时间
                r为range，range=0.5,为选取的数据范围，可以是(0:1),range越大，选取的数据越少
                statu=1 对应着为原始数据
            Output parameter：
                min_position最小值的位置
                max_position最大值的位置
        """
        whole_img_data = self.data[1:, 1:]

        y_data = whole_img_data.sum(1)
        y_data = y_data / np.max(y_data)

        # 获取最小值
        min_y_position_list = np.where(y_data > self.y_range)

        for i in np.arange(np.size(min_y_position_list[0])):
            if (min_y_position_list[0][i + 1] - min_y_position_list[0][i] == 1
                    and min_y_position_list[0][i + 2] - min_y_position_list[0][i + 1] == 1):
                self.min_y_position = min_y_position_list[0][i]
                print(self.min_y_position)
                break

        # 获得最大值的位置
        max_y_position_list = np.where(y_data[self.min_y_position:] < self.y_range)
        for j in np.arange(len(max_y_position_list[0])):
            if (max_y_position_list[0][j + 1] - max_y_position_list[0][j] == 1
                    and max_y_position_list[0][j + 2] - max_y_position_list[0][j + 1] == 1):
                self.max_y_position = max_y_position_list[0][j] + self.min_y_position
                break

    def move_data_time(self, cur_pos=166, pur_pos=130):
        """
            对原始的数据进行移动
        :param cur_pos: 当前位置
        :param pur_pos: 目标位置
        :return:移动后的数据
        """

        distance = cur_pos - pur_pos
        rows, cols = self.data.shape
        # 构建移动后的数据
        move_data = self.data

        if distance >= 0:  # 往前移动
            # 选取要移动的数据
            ori_part_data = self.data[distance:, 1:]
            # 把选取出来的部分数据赋给move_data
            move_data[:rows - distance, 1:] = ori_part_data
        else:
            # 选取要移动的数据
            ori_part_data = self.data[1: distance, 1:]
            # 把选取出来的部分数据赋给move_data
            move_data[-distance + 1:, 1:] = ori_part_data
        return move_data

    def plot_spec_image(self):
        """
            画出光谱图像
            Input parameter:
                data为原始数据，为矩阵，第一行和第一列分别为波长和时间
                y_min, y_max,为调用函数get_ymin_ymax分析后的结果

        """
        image_data = self.data[self.min_y_position:self.max_y_position, 1:]
        print(image_data.shape)
        plt.subplot(121)
        plt.imshow(image_data, cmap=plt.cm.jet)

        plt.subplot(122)
        Y = image_data.sum(0)
        Y = Y / np.max(Y)
        X = self.data[0, 1:]
        center_wavelength = X[Y.argmax()]
        plt.plot(X, Y, label="%.1f nm" % center_wavelength)
        plt.legend()

    def plot_time_image(self, l_label=None, style='-'):
        """
            画出寿命图像
            Input parameter:
                data为原始数据，为矩阵，第一行和第一列分别为波长和时间
                x_min, x_max,为调用函数get_xmin_xmax分析后的结果
        """
        image_data = self.data[1:, self.min_x_position:self.max_x_position]
        rows, cols = image_data.shape
        # plt.figure('lifetime')
        # plt.figure(figsize=(10, 5))
        # plt.subplot(121)
        # plt.imshow(image_data, cmap=plt.cm.jet)

        # plt.subplot(111)
        Y = image_data.sum(1) / cols
        Y = Y / np.max(Y)
        X = self.data[1:, 0]
        # 计算寿命
        # lifetime = get_lifetime(X, Y)
        # plt.plot(X, Y, label=l_label + "  Lifetime: %.2f ps" % lifetime)
        plt.plot(X, Y, style, label=l_label, linewidth=2)
        plt.xlim(0, 60)
        # plt.ylim(0, max(Y)*1.01)
        plt.xlabel('Time (ps)')
        plt.ylabel('PL Intensity')
        plt.legend()

    @staticmethod
    def poly_fit(self, x, y, number=1):
        """
            多项式曲线拟合
            Input parameter:
                x,y两个向量，number为拟合阶数，默认为1，为线性拟合
            Output parameter：
                y_vals为拟合后对应的y数据
        """
        z1 = np.polyfit(x, y, number)  # 获得拟合系数
        p1 = np.poly1d(z1)  # 形成拟合函数
        print(p1)
        y_vals = p1(x)  # 使用拟合函数求y的拟合值
        return y_vals

    def read_max_data(self):
        """
            获取最大值对应的时间，获取最大值对应的波长，获取最大值
            Input parameter：
                ori_data为原始数据，为矩阵，第一行和第一列不是数据，分别为波长和时间
            Output parameter：
                time：最大值对应的时间
                wavelength：最大值对应的波长
                max_data：最大值
        """
        ori_data = np.double(self.data)  # 数据类型转换
        data = ori_data[1:, 1:]

        arg_max = np.argmax(data)  # 获取最大值的位置
        row = arg_max // data.shape[1]  # 获取最大值所在的行
        col = arg_max % data.shape[1]  # # 获取最大值所在的列
        max_data = np.max(data)
        # max_data1 = data[row, col]

        time = ori_data[row + 1, 0]  # 获取最大值对应的时间
        wavelength = ori_data[0, col + 1]  # 获取最大值对应的波长
        return time, wavelength, max_data

    def show_image(self):
        """
            显示图片
            Input parameter：
                data为包括第一行喝第一列的原始数据
        """
        image_data = self.data[1:, 1:]
        #    image_data = image_data.astype(np.uint8)
        plt.imshow(image_data, cmap=plt.cm.jet)  # 显示图像，坐标位置
        plt.show()

    def subtract_background(self, extend=190):

        """
        数据减去背景
        :param ori_data: 输入的数据
        :param stu: 状态默认为1，包含第一行喝第一列
        :param extend: 额外减去的部分
        :return: 返回减去背景的数据
        """
        self.data[1:, 1:] = self.data[1:, 1:] - np.min(self.data[1:, 1:]) - extend
        return self.data


if __name__ == '__main__':
    # filenames = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\条纹相机" \
    #            r"\quantum dots1\800+400double_pulse\one\chun_400_ji_she_(andor)\dac\alter\2_28.dat"
    # datas = load_dat_data(filenames)
    # show_image(datas)
    pass
