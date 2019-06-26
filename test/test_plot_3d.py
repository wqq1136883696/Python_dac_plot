# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 21:54:17 2019

@author: wyatt

The purpose of the script is ... 
"""

#画三维图
import  numpy  as  np
from    mpl_toolkits.mplot3d  import Axes3D
from pylab import  *
fig=figure()
ax=Axes3D(fig)
x=np.arange(-4,4,0.1)
y=np.arange(-4,4,0.1)
x,y=np.meshgrid(x,y)
R=np.sqrt(x**2+y**2)
z=np.sin(R)
ax.plot_surface(x,y,z,rstride=1,cstride=1,cmap='hot')
show()
