# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 10:31:33 2019

@author: wyatt

This script can load an Excel data table and plot the relationship between PL intensity and excitation power.
这个脚本可以加载一个Excel的数据表，然后画出PL强度与激发功率的关系。
"""

import numpy as np
import matplotlib.pyplot as plt
from wyatt_function import load_xlsx

   
def main():
    filename = (r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\Tm_quantum dots1"
                r"\800+400double_pulse\one\double_800 jia 400 bian power\alter\change_power.xlsx")
    sheet = load_xlsx(filename)
    power = np.array(sheet.col_values(1)[1:])
    max_data = np.array(sheet.col_values(4)[1:])
    max_data = max_data / np.max(max_data)

    # 画PL强度与激发功率的关系
    fig = plt.figure()
    plt.plot(power, max_data, '*')
    plt.xlabel('Excitation Power (mW)')
    plt.ylabel('PL Intensity (a.u.)')
    plt.ylim(0, 1.02)
    plt.xlim(0, 17)
    plt.show()
    

if __name__ == '__main__':
    plt.close('all')
    main()
