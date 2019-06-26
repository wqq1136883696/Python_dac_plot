#! /usr/bin/python3
# coding : utf-8

"""
Created on Thu Mar 14 10:31:33 2019

@author: wyatt

1.读取folder_path文件夹下的dac文件列表
2.读取每一个dac文件的内容，保存到矩阵
3.然后把矩阵保存到.dat文件
"""

import os
from wyatt_function import show_file, load_dac_file, show_folder


def loop_folder(pub_folder):
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
                
            loop_folder(pub_folder + "\\" + folder)  # 循环调用自身
           


if __name__ == '__main__':
    # Windows平台
    folders = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\Tm_quantum dots1\change temperture"
    loop_folder(folders)

    
             
            

