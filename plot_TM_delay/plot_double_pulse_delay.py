#! /usr/bin/python3
# coding : utf-8
"""
Created on Thu Mar 14 10:31:33 2019

@author: wyatt

This script can load an txt format data and plot the relationship between PL intensity and excitation power.
这个脚本可以加载一个txt的数据，然后画出PL强度与激发功率的关系。
"""

from wyatt_function import *
import matplotlib.pyplot as plt
import os


def main(floder):
    file_list = show_file(floder + "\\alter", fmt='.dat')
    for file in file_list:
        print(file)
        data = load_dat_data(floder + "\\alter\\" + file)

        # show_image(data)
        xmin, xmax = get_xmin_xmax(data, r=0.3)
        plot_time_image(data, xmin, xmax)
        plt.savefig(floder + "\\image\\" + file.split('.dat')[0] + ".png")
        # plt.show()


if __name__ == '__main__':
    floders = (r"G:\Group_Work\Wyatt_Experiment\Quantum_dot"
               r"\Tm_quantum dots1\800+400double_pulse\one\double_800 jia 400 bian power")
    os.mkdir(floders + "\\image")
    main(floders)

