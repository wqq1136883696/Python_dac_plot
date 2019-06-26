# -*- coding: utf-8 -*-

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

import os
import xlrd
import numpy as np


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


def load_dat_data(filename):
    """
        读取dat文件中的数据，转换成浮点矩阵
        Input parameter：
            filename为文件路径
    """
    data = np.loadtxt(filename)  # 加载文件数据，读取的为字符串
    data = data.astype(np.float32)  # 转换成浮点矩阵
    return data


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


def loop_folder_dac2dat(pub_folder):
    """
        这个函数调用show_folder, show_file, load_dac_file,
        然后可以实现把pub_folder文件夹下的所有的dac文件夹中的dac文件转换成
        dat文件（以numpy数组的形式保存的，并且把第一行第一列的ps|nm换成0），
        可以使用np.loadtxt()直接读取

        采用的python递归的方法实现程序目标
    :param pub_folder: 文件夹路径
    :return:
    """
    folder_list = show_folder(pub_folder)
    if len(folder_list) > 0:  # 如果子文件夹存在，则循环显示子文件夹中的文件
        for folder in folder_list:

            if folder == 'dac':  # 如果文件夹为dac,则进行数据处理
                dac_filename_list = show_file(pub_folder + "\\" + folder)  # 显示dac文件列表

                if 'alter' in folder_list:  # 如果alter文件夹已经存在，显示dat列表
                    dat_filename_list = show_file(pub_folder + "\\alter", fmt='.dat')
                else:  # 否则新建alter文件夹
                    os.mkdir(pub_folder + "\\alter")
                    dat_filename_list = []

                if len(dat_filename_list) == 0:  # 如果列表为空，则进行数据保存
                    for filename in dac_filename_list:  # 进行保存数据的操作
                        load_dac_file(pub_folder, filename)

            loop_folder_dac2dat(pub_folder + "\\" + folder)  # 循环调用自身


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


def show_folder(folder_path):
    """
        显示folder_path下的文件夹列表
    :param folder_path: 文件夹地址
    :return:folder_list：文件夹列表
    """
    folder_list = []
    dirs = os.listdir(folder_path)

    for file in dirs:  # 循环读取路径下的文件并筛选输出
        filename = file.split('.')
        size = len(filename)
        if size == 1:  # 筛选文件夹
            folder_list.append(file)
        elif size > 1:
            if filename[size-1][0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                folder_list.append(file)

    return folder_list


sub_folder = []


def show_all_sub_folder(pub_folder, name="dac"):
    """
    显示所有的子文件夹
    :param pub_folder: 父文件夹
    :param name: 要选择的文件夹
    :return: sub_name 所有名为name的子文件夹
    """
    if name == "dac":
        folder_list = show_folder(pub_folder)
        if len(folder_list) > 0:  # 如果子文件夹存在，则循环显示子文件夹中的文件
            for folder in folder_list:
                if folder == name:  # 如果文件夹为dac,则保存起来
                    sub_folder.append(pub_folder + "\\" + folder)  # 显示dac文件列表

                show_all_sub_folder(pub_folder + "\\" + folder, name)  # 循环调用自身
    else:
        folder_list = show_folder(pub_folder)
        if len(folder_list) > 0:  # 如果子文件夹存在，则循环显示子文件夹中的文件
            for folder in folder_list:
                sub_folder.append(pub_folder + "\\" + folder)  # 显示dac文件列表
                show_all_sub_folder(pub_folder + "\\" + folder, name)  # 循环调用自身

    return sub_folder
