#! /usr/bin/python3
# coding : utf-8
import numpy as np
from wyatt_function import show_file, read_max_data


def main():
    """
        获取选定文件夹下所有dat数据文件的最大值，
        对应的波长，对应的时间，保存到文件
    """
    folder = (r'G:\Group_Work\Wyatt_Experiment\Quantum_dot\Tm_quantum dots1'
              r'\800+400double_pulse\three\800shuang guang zi\alter')
    dat_list = show_file(folder, fmt='.dat')  # 显示文件列表
    
    times = []
    wavelengths = []
    max_datas = []
    
    for dat_file in dat_list:
        dat_data = np.loadtxt(folder+"\\"+dat_file)
        time, wavelength, max_data = read_max_data(dat_data)
        times.append(time)
        wavelengths.append(wavelength)
        max_datas.append(max_data)
        print("filename , %s  ,time , %.5f,  wavelength , %.5f,"
              "max_data , %.5f" % (dat_file, time, wavelength, max_data))
        
    max_data_whole = np.vstack((np.array(times), 
                               np.array(wavelengths), np.array(max_datas)))
    np.savetxt(folder+"\\max.txt", max_data_whole, delimiter='\t', fmt='%.5f')
             
    
if __name__ == '__main__':
    main()
