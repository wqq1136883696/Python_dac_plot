import numpy as np
import os
import matplotlib.pyplot as plt
from wyatt_modules import FileProcess as fp
from wyatt_modules import DataProcess as dp


def create_time(STATE):
    folder = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\20190505\20ps\interference\alter"
    file_list = fp.show_file(folder, fmt=".dat")
    for file in file_list:
        data = fp.load_dat_data(folder + "\\" + file)
        if STATE:
            print(file)
            dp.show_image(data)
        else:
            x_min, x_max = dp.get_xmin_xmax(data)
            X, Y = dp.plot_time_image(data, x_min, x_max, l_label=file)
            size = len(X)
            save_data = np.zeros((size, 2))
            save_data[:, 0] = X
            save_data[:, 1] = Y
            try:
                os.mkdir(folder + "\\time")
            except FileExistsError:
                pass
            # np.savetxt(folder + "\\time\\time_" + file, save_data, fmt='%s', delimiter='\t')
            plt.savefig(folder + "\\time\\" + str(file.split(".")[:-1]), fmt='jpg')
    plt.show()


def imshow():
    folder = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\20190505\40ps\interference\alter"
    file_list = fp.show_file(folder, ".dat")

    for file in file_list[2:3]:
        print(file)
        data = fp.load_dat_data(folder + "\\" + file)
        dp.show_image(data)

    plt.show()


create_time(STATE=1)
# imshow()
