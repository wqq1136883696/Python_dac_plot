# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 19:55:06 2019

@author: wyatt

The purpose of the script is ... 
"""

import numpy as np
import matplotlib.pyplot as plt
import wyatt_modules.FileProcess as fp
import wyatt_modules.DataProcess as dp


def image_plot(data, x_min, x_max, l_label=None, style='-'):
    image_data = data[1:, x_min:x_max] - 30
    ap = image_data >= 0
    image_data = image_data * ap
    rows, cols = image_data.shape
    # plt.figure('lifetime')
    # plt.figure(figsize=(10, 5))
    # plt.subplot(121)
    # plt.imshow(image_data, cmap=plt.cm.jet)

    # plt.subplot(111)
    Y1 = image_data.sum(1)
    Y = Y1 / cols
#    Y = Y / np.max(Y)
    X = data[1:, 0]
    
    # 计算寿命
    #lifetime = get_lifetime(X, Y)
    # plt.plot(X, Y, label=l_label + "  Lifetime: %.2f ps" % lifetime)
    plt.plot(X, Y, style, label=l_label, linewidth=2)
    plt.xlim(0, 60)
    # plt.ylim(0, max(Y)*1.01)
    plt.xlabel('Time (ps)')
    plt.ylabel('PL Intensity')
    plt.legend()


def change_name(file_name):
    """
        temp为把'_'和'-'换成'.'后的字符串
    """
    temp = file_name.split('.dat')[0]
    if temp[-1] == 'K':
        temp = temp[0:-1]
    
    if temp.find('_') > 0:
        temp_list = temp.split('_')
        temp = temp_list[0] + "." + temp_list[1]
       
    if temp.find('-') > 0:
        temp_list = temp.split('-')
        temp = temp_list[0] + "." + temp_list[1]
    return temp
    

def spec_plot(data, y_min, y_max, filename=None):
    
    image_data = data[y_min:y_max, 1:]
    rows,cols = image_data.shape
    print(rows,cols)
#    plt.subplot(121)
#    plt.imshow(image_data, cmap=plt.cm.jet)
    
    plt.xlim(525, 540)
    plt.subplot(111)
    Y = image_data.sum(0) / rows
#    Y = Y / np.max(Y)
    X = data[0, 1:]
    
    # 修改文件名
    temp = '0'
    
    if filename:
        temp = change_name(filename)
    
    center_wavelength = X[Y.argmax()]
    plt.plot(X, Y, label="P:{:s}um        {:.1f}nm".format(temp, center_wavelength))
    plt.legend()
    return temp, center_wavelength, Y.max()


folder = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\Tm_quantum dots1"
sub_folder = r"\800+400double_pulse\3\400+800change800power\alter"
whole_folder = folder + sub_folder
file_list = fp.show_file(whole_folder, '.dat')


temp_wave_data = np.zeros((len(file_list), 3))
i = 0
for file_name in file_list:
#    if i in [19]:
    data = fp.load_dat_data(whole_folder + "\\" + file_name)
##        xmin, xmax = dp.get_xmin_xmax(data)
##        image_plot(data, xmin, xmax, l_label="T:{:s}K".format(file_name.split('.dat')[0]), style="-")
    ymin, ymax = dp.get_ymin_ymax(data)
    temp1, center_wavelength1, y_max = spec_plot(data, ymin, ymax, filename=file_name)
    temp_wave_data[i, :] = [float(temp1), center_wavelength1, y_max]
    
    i += 1
    
np.savetxt(whole_folder + "\\power_wave_data.csv", temp_wave_data, fmt='%.2f', delimiter=',')
     
     
     
     
        