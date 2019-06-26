import numpy as np
import time
from multiprocessing import Pool
from wyatt_modules import FileProcess as fp

"""
    使用多进程运行,速度比较快
"""


# 背景图片
background = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\20190505\alter_1\background.dat"
bg_data = fp.load_dat_data(background)

i = 0


def subtract_background(folder):
    sub_folder = fp.show_all_sub_folder(folder, name="alter")
    po = Pool(4)
    for sub in sub_folder:
        po.apply_async(sub_bg, (sub, ))

    print("----start----")
    po.close()  # 关闭进程池，关闭后po不再接收新的请求
    po.join()  # 等待po中所有子进程执行完成，必须放在close语句之后
    print("\n-----end-----")


def sub_bg(sub):
    """
        sub文件夹下的文件去背景
    :param i: 文件数目
    :param sub: 文件夹路径
    """
    global i
    dat_file = fp.show_file(sub, fmt=".dat")
    for file in dat_file:
        ori_data = fp.load_dat_data(sub+"\\"+file)
        data = ori_data.copy()
        # print(np.average(ori_data[1:, 3]))
        if np.average(ori_data[1:, 3]) > 500:
            data[1:, 1:] = ori_data[1:, 1:] - bg_data[1:, 1:]
            np.savetxt(sub+"\\"+file, data, fmt='%s', delimiter='\t')
        i += 1
        print("\r***已完成   {}  个文件, 平均值为{} ***".format(i, np.average(ori_data[1:, 3])), end="")


def main(folder):
    print("--------开始去背景---------")
    subtract_background(folder)
    print("\n--------已全部完成去背景---------")


if __name__ == '__main__':
    # 加载数据文件，然后去背景
    folder = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\20190505"
    start = time.perf_counter()
    main(folder)
    print("用时：{:.3f}s".format(time.perf_counter()-start))
