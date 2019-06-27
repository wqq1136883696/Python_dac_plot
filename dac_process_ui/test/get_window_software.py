# -*- coding: UTF8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import _winreg
import re, sys, os, rcc
import win32ui

import win32gui

reload(sys)

sys.setdefaultencoding("utf-8")
class ListDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(ListDialog, self).__init__(parent)
        self.contentsWidget = QtGui.QListWidget()
        self.contentsWidget.setViewMode(QtGui.QListView.IconMode)
        self.contentsWidget.setIconSize(QtCore.QSize(96, 84))  # Icon 大小
        self.contentsWidget.setMovement(QtGui.QListView.Static)  # Listview不让列表拖动
        self.contentsWidget.setMaximumWidth(800)  # 最大宽度
        self.contentsWidget.setSpacing(15)  # 间距大小
        winrege = winregeditor()
        self.numreg = winrege.getreg()
        for key in self.numreg.keys():
            Atem = QtGui.QListWidgetItem(self.contentsWidget)
            try:  # ico 来自exe
                large, small = win32gui.ExtractIconEx(self.numreg[key]['exe'], 0)
                exeMenu = self.numreg[key]['exe']
                win32gui.DestroyIcon(small[0])
                self.pixmap = QtGui.QPixmap.fromWinHBITMAP(self.bitmapFromHIcon(large[0]), 2)
            except Exception as err:  # ico 来自 icon
                if self.numreg[key].has_key('icon') and os.path.isfile(self.numreg[key]['icon']):  # 判断ico文件是否存在
                    self.pixmap = QtGui.QPixmap(self.numreg[key]['icon'])
                    iconMenu = self.numreg[key]['icon']
                    split = iconMenu.split('\\')
                    exeMenu = '\\'.join(split[:-1])
                else:  # 不存在ico文件给定默认图标
                    self.pixmap = ':default.png'
                    exeMenu = ''

                Atem.setIcon(QtGui.QIcon(self.pixmap))
                Atem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                Atem.setTextAlignment(QtCore.Qt.AlignHCenter)
                Atem.setData(QtCore.Qt.UserRole, exeMenu)
                DisplayName = self.numreg[key]['DisplayName'].encode('utf-8')
                Atem.setToolTip(u"" + DisplayName)  # tip 显示
                if len(DisplayName) >= 6:
                    DisplayName = DisplayName.decode('utf8')[0:6].encode('utf8') + '…'
                Atem.setText(u"" + DisplayName)

