#! /usr/bin/python3
# coding : utf-8

"""
Created on Thu Apr 1 13:10:33 2019

@author: wyatt

1.读取folder文件夹下的dac文件列表
2.读取每一个dac文件的内容，保存到矩阵
3.然后把矩阵保存到.dat文件
"""

import data_process.FileProcess as fp


def main():
    folder = r"G:\Group_Work\Wyatt_Experiment\NanoSheets\TW\tangbing_sample\ColdTemp"
    fp.loop_folder_dac2dat(folder)


if __name__ == '__main__':
    main()
