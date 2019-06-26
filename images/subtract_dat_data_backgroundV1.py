import numpy as np
import time
from wyatt_modules import FileProcess as fp

# 背景图片
background = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\20190505\alter_1\background.dat"
bg_data = fp.load_dat_data(background)


def subtract_background(folder):
    sub_folder = fp.show_all_sub_folder(folder, name="alter")
    i = 0
    for sub in sub_folder:
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
