# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 18:03:06 2019

@author: wyatt

The purpose of the script is ... 
"""

import matplotlib.pyplot as plt
import mpl_toolkits.axisartist.axislines as aa
import wyatt_modules.FileProcess as fp
import wyatt_modules.DataProcess as dp


folder = r"G:\Group_Work\Wyatt_Experiment\Quantum_dot\Tm_quantum dots1"
sub_folder = r"\change temperture\2\alter"
whole_folder = folder + sub_folder
file_list = fp.show_file(whole_folder, '.dat')

fig = plt.figure()
ax = aa.SubplotZero(fig, 1, 1, 1)
fig.add_subplot(ax)

data = fp.load_dat_data(whole_folder + "\\" + file_list[0])
xmin, xmax = dp.get_xmin_xmax(data)
dp.plot_time_image(data, xmin, xmax, l_label="T:{:s}".format(file_list[0]), style="r-")
ax1 = plt.gca()

#offset = (40, 0)
#ax1.xaxis.set_ticks_position('bottom')
#ax1.spines['bottom'].set_position(('axes',0.5))
ax.set_ylim([0, 5])
ax.axis["line1"] = ax.new_floating_axis(nth_coord=0, value=1.2, axis_direction="bottom")
ax.axis["line1"].toggle(all=True)
ax.axis["line1"].label.set_visible(False)
ax.axis["line1"].major_ticklabels.set_visible(False)
#ax.axis["line1"].label.set_color('blue')

#
#offset = (40, 0)
#new_axisline = ax.get_grid_helper().new_fixed_axis
#ax.axis["新建2"] = new_axisline(loc="right", offset=offset, axes=ax)
#ax.axis["新建2"].label.set_text("新建纵坐标")
#ax.axis["新建2"].label.set_color('red')
#

