import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from data_process import StripeCamera
from Ui_stripe_camera import Ui_MainWindow


# 创建一个matplotlib图形绘制类
class MyFigure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        # 第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # 第二步：在父类中激活Figure窗口
        super(MyFigure, self).__init__(self.fig)  # 此句必不可少，否则不能显示图形
        # 第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)

    # 第四步：就是画图，【可以在此类中画，也可以在其它类中画】
    def plot_show(self):
        self.axes0 = self.fig.add_subplot(111)
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.axes0.plot(t, s)

    def image_show(self, image_data):
        """显示图像"""
        self.axes.imshow(image_data)


class MainWindow(QMainWindow, Ui_MainWindow, QTreeView):
    """主窗口"""
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        # 文件选择框
        self.folder_tree = TreeView()
        self.folder_tree.setPath(r"G:\Group_Work\Wyatt_Experiment\NanoSheets\TW\tangbing_sample\ColdTemp")
        self.folder_widget.addWidget(self.folder_tree)
        self.folder_tree.Signal_NoParameters.connect(self.differentiate_file_formats)

        # 变量
        self.data = None
        self.fig = None
        # 调用初始化方法
        self.init()

    def init(self):
        """初始化一些按钮 """
        self.upper_level_Button.clicked.connect(self.upper_level)

    def closeEvent(self, close_event):
        """关闭事件"""
        reply = QMessageBox.question(self, '警告', '客官，您真的要走了吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            close_event.accept()
            self.stop_remote_app()
        elif reply == QMessageBox.No:
            close_event.ignore()

    def upper_level(self):
        """上一级文件"""
        cur_path = self.folder_tree.getCurPath()
        print(cur_path)
        path_list = cur_path.split("/")
        parent_path = ""
        if os.path.isdir(cur_path):
            for path_part in path_list[:-1]:
                path_part += "/"
                parent_path += path_part
        else:
            for path_part in path_list[:-2]:
                path_part += "/"
                parent_path += path_part
        print(parent_path)
        self.folder_tree.setPath(parent_path)

    def differentiate_file_formats(self):
        """区分不同文件格式"""
        cur_path = self.folder_tree.getCurPath()
        my_path_list = os.path.splitext(cur_path)
        # print(my_path_list)
        if my_path_list[1] == ".dat":
            self.load_dat(cur_path)
        elif my_path_list[1] == ".asc":
            # TODO 加载asc
            pass

    def load_dat(self, my_path):
        """加载dat数据"""
        # TODO 加载dat
        if self.fig:
            self.image_layout.removeWidget(self.fig)
        my_path_list = os.path.split(my_path)
        self.data = StripeCamera.load_dat_data(my_path)
        image_data = self.data[1:, 1:]
        # 图窗实例
        # 第五步：定义MyFigure类的一个实例
        self.fig = MyFigure()
        self.fig.image_show(image_data)
        self.fig.axes.grid(False)
        self.fig.mpl_connect('button_press_event', self.on_mouse_press)
        self.fig.drawRectangle()
        # 第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        self.image_layout.addWidget(self.fig)

    def on_mouse_press(self, event):
        """鼠标点击事件"""
        position = "current position: mouse={}, x={:.2f}, y={:.2f}".format(event.button, event.xdata, event.ydata)
        print(position)
        self.position_lineEdit.setText(position)
        if self.line_tool.isChecked():
            self.fig.draw

    def update_line_image(self):
        """更新图像"""
        if self.fig:
            self.image_layout.removeWidget(self.fig)
        self.fig.axes.vlines()
        self.image_layout.addWidget(self.fig)


class TreeView(QTreeView):
    # 信号
    Signal_NoParameters = pyqtSignal()

    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)

        self.__model = QFileSystemModel()
        self.__model.setRootPath(QDir.rootPath())
        self.setModel(self.__model)
        self.setColumnWidth(0, 200)
        self.data = None

        self.__current_select_path = None
        self.doubleClicked.connect(self.__getCurPathEvent)

    # 双击信号 获得当前选中的节点的路径
    def __getCurPathEvent(self):
        index = self.currentIndex()
        model = index.model()  # 请注意这里可以获得model的对象
        self.__current_select_path = model.filePath(index)
        if os.path.isdir(self.__current_select_path):
            # 可以设置当前根目录
            self.setPath(self.__current_select_path)
        else:
            # TODO 针对不同文件有不同的方法
            self.Signal_NoParameters.emit()

    # 设置TreeView的跟文件夹
    def setPath(self, path):
        self.setRootIndex(self.__model.index(path))

    # 获得当前选中的节点的路径
    def getCurPath(self):
        return self.__current_select_path


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = MainWindow()
    windows.show()
    sys.exit(app.exec_())
