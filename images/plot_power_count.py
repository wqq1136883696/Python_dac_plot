#! /usr/bin/python3
# coding : utf-8
"""
Created on Thu Mar 14 10:31:33 2019

@author: wyatt

This script can load an txt format data and plot the relationship between PL intensity and excitation power.
这个脚本可以加载一个txt的数据，然后画出PL强度与激发功率的关系。
"""

import numpy as np
import matplotlib.pyplot as plt
from wyatt_function import polyfit, load_xlsx


def load_data(filename):
    """加载数据"""
    folder = (r"G:\Group_Work\Wyatt_Experiment\Quantum_dot"
              r"\Tm_quantum dots1\800+400double_pulse\three\400change power\alter")
    if filename.split('.')[-1] in ['txt', 'dat']:
        txt_data = np.loadtxt(folder + "\\" + filename)
    elif filename.split('.')[-1] == 'xlsx':
        txt_data = load_xlsx(folder + "\\" + filename)

    return txt_data, filename.split('.')[-1]
    

def plot(x, y, x_label='Excitation Power (mW)', y_label='PL Intensity (a.u.)'):
    plt.figure(1)

    plt.plot(x, y, '*', label='original')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(0, max(x)*1.1)
    plt.ylim(0, max(y)*1.1)
    
    yvals = polyfit(x, y, 2)
    
    plt.plot(x, yvals, 'r', label='polyfit values')
    plt.legend()
    
    plt.show()
    
    
if __name__ == '__main__':
    plt.close('all')
    data, fmt = load_data('max_data.xlsx')
    if fmt == 'xlsx':
        power = np.array(data.col_values(1)[1:])
        max_data = np.array(data.col_values(4)[1:])
        max_data = max_data / np.max(max_data)
        plot(power, max_data)
    else:
        x_data = data[3, :]
        y_data = data[2, :] / np.max(data[2, :])
        plot(x_data, y_data)
