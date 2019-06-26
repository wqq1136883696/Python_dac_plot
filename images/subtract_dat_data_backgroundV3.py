import numpy as np
import time
# from multiprocessing import Pool
from threading import Thread, Lock
from wyatt_modules import FileProcess as fp

"""
    使用多线程运行
"""


class MyThread(Thread):
    def __init__(self, sub):
        super().__init__()
        self.sub = sub
        self.i = 0
        self.mutex = Lock()

    def run(self):
        """
        sub文件夹下的文件去背景
        :param
        sub: 文件夹路径
        """
        dat_file = fp.show_file(self.sub, fmt=".dat")
        for file in dat_file:
            ori_data = fp.load_dat_data(self.sub+"\\"+file)
            data = ori_data.copy()
            # print(np.average(ori_data[1:, 3]))
            if np.average(ori_data[1:, 3]) > 500:
                data[1:, 1:] = ori_data[1:, 1:] - bg_data[1:, 1:]
                np.savetxt(self.sub+"\\"+file, data, fmt='%s', delimiter='\t')
            metex_flag = self.mutex.acquire(False)
            if metex_flag:
                self.i += 1
                self.mutex.release()

            print("\r***已完成   {}  个文件, 平均值为{} ***".format(self.i, np.average(ori_data[1:, 3])), end="")


# 背景图片
background = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\20190505\alter_1\background.dat"
bg_data = fp.load_dat_data(background)


def subtract_background(folder):
    sub_folder = fp.show_all_sub_folder(folder, name="alter")
    for sub in sub_folder:
        t = MyThread(sub)
        t.start()


def main(folder):
    print("--------开始去背景---------")
    subtract_background(folder)
    print("\n--------已全部完成去背景---------")


if __name__ == '__main__':
    # 加载数据文件，然后去背景
    folders = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\20190505"
    start = time.perf_counter()
    main(folders)
    print("用时：{:.3f}s".format(time.perf_counter()-start))
