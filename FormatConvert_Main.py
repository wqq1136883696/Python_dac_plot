""""""
import sys
from os import path
import time
from threading import Thread
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from FormatConvertTools import Ui_MainWindow
# from StripeCameraComm import StpCaComm
from data_process import FileProcess as FP
import Remote_Converter_format as rcf


class MainWindow(QMainWindow, Ui_MainWindow):
    """显示窗体"""
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.str_cam_app = None
        self.can_control = False
        self.all_list = []
        self.error_list = []
        self.start_convert_timer = QTimer()
        self.is_start_convert = False
        self.for_convert = Thread(target=self.format_convert)
        self.recv_response = None

        # 初始化按钮方法
        self.init()

    def init(self):
        """初始化按钮"""
        self.startApp_pushButton.clicked.connect(self.start_remote_app)
        self.closeApp_pushButton.clicked.connect(self.stop_remote_app)
        self.folder_pushButton.clicked.connect(self.get_folder)
        self.start_format_convert_pushButton.clicked.connect(self.start_convert)
        self.stop_format_convert_pushButton.clicked.connect(self.stop_convert)
        self.for_convert.setDaemon(False)
        self.for_convert.start()
        # self.set_can_control(True)

    def closeEvent(self, closevent):
        """关闭程序"""
        reply = QMessageBox.question(self, '警告', '客官，您真的要走了吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("再见")
            closevent.accept()
            self.stop_remote_app()
        elif reply == QMessageBox.No:
            closevent.ignore()

    def set_can_control(self, status):
        """设置能够控制"""
        self.can_control = status
        self.format_groupBox.setEnabled(self.can_control)
        self.all_groupBox.setEnabled(self.can_control)
        self.error_groupBox.setEnabled(self.can_control)
        self.command_comboBox.setEnabled(self.can_control)
        # self.textEdit.setEnabled(self.can_control)
        self.startApp_pushButton.setEnabled(not self.can_control)
        self.closeApp_pushButton.setEnabled(self.can_control)
        # self.start_format_convert_pushButton.setEnabled(self.can_control)
        # self.stop_format_convert_pushButton.setEnabled(self.can_control)

    def start_remote_app(self):
        """开启远程应用"""
        try:
            self.str_cam_app = rcf.StpCaComm()  # 远程使用格式转换app
        except Exception as err:
            self.textEdit.insertPlainText("连接错误：{}".format(err))
        else:
            self.textEdit.insertPlainText("已连接到目标计算机:\n")
            self.textEdit.insertPlainText(self.str_cam_app.receive())

            # 创建线程
            rec = rcf.Thread(target=rcf.receive, args=(self.str_cam_app,))
            rec.setDaemon(False)
            rcf.thread_status = True
            rec.start()
        try:
            self.str_cam_app.send_command_get_response("AppStart()")
            response = rcf.recv_response()
            print(response)
            self.textEdit.insertPlainText(response)
            i = 0
            while response[0] != "0":
                response = rcf.recv_response()
                print(response)
                self.textEdit.insertPlainText(response)
                i += 1
                if i == 5:
                    break
            print(response[0])
            if response[0] == "0":
                self.set_can_control(True)
            else:
                self.set_can_control(False)
        except Exception as err:
            print(err)
        self.recv_response = Thread(target=rcf.receive, args=(self.str_cam_app,))
        self.recv_response.setDaemon(False)
        self.recv_response.start()

    def stop_remote_app(self):
        """结束远程app"""
        self.str_cam_app.send_command_get_response("AppEnd()")
        response = rcf.recv_response()
        print(response)
        self.textEdit.insertPlainText(response)
        while response[0] != "0":
            if response[0] == "3":
                break
            response = rcf.recv_response()
            print(response)
            self.textEdit.insertPlainText(response)
        if response[0] == "0" or response[0] == "3":
            self.set_can_control(False)
        else:
            self.set_can_control(True)
        try:
            self.str_cam_app.close()
        except Exception as err:
            print(err)
        finally:
            rcf.thread_status = False
            pass

    def get_format(self):
        """获取源格式，和目标格式"""
        original_format = self.orignal_comboBox.currentText()
        ori_format = original_format[1:]
        target_format = self.target_comboBox.currentText()
        tar_format = target_format[1:]
        return ori_format, tar_format

    def get_folder(self):
        """获得文件夹下的所有内容"""
        ori_format, tar_format = self.get_format()
        # print(ori_format, tar_format)
        folder = QFileDialog.getExistingDirectory(self, "选取文件夹",
            r"G:\Group_Work\Wyatt_Experiment\NanoSheets\TW\tangbing_sample\NormalTemp")
        if folder:
            self.folder_lineEdit.setText(folder)
            folder_list = FP.show_all_sub_folder(folder, name=None)
            # print(folder_list)

            self.all_tableWidget.setColumnCount(2)
            width = self.all_tableWidget.width()
            self.all_tableWidget.setColumnWidth(0, width/1.4)
            self.all_tableWidget.setColumnWidth(1, width-width/1.36)
            self.all_tableWidget.horizontalHeader().setVisible(False)
            self.all_tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            count = 0
            for sub_folder in folder_list:
                file_list = FP.show_file(sub_folder, fmt=ori_format)
                for file in file_list:
                    # print(file)
                    count += 1
            self.all_tableWidget.setRowCount(count)

            i = 0
            for sub_folder in folder_list:
                file_list = FP.show_file(sub_folder, fmt=ori_format)
                for file in file_list:
                    self.all_list.append("{}/{}".format(sub_folder, file))
                    self.all_tableWidget.setItem(i, 0, QTableWidgetItem(sub_folder))
                    self.all_tableWidget.setItem(i, 1, QTableWidgetItem(file))
                    i += 1

            self.start_format_convert_pushButton.setEnabled(True)

    @staticmethod
    def get_target_format(tar_format):
        """获取目标格式"""
        t_format = "asciical"
        suffix = ".dac"
        if tar_format == ".dac":
            t_format = "asciical"
            suffix = ".dac"
        elif tar_format == ".img":
            t_format = "img"
            suffix = ".img"
        elif tar_format == ".tif":
            t_format = "tif"
            suffix = ".tif"
        elif tar_format == ".dat":
            t_format = "ascii"
            suffix = ".dat"
        elif tar_format == ".tiff":
            t_format = "tiff"
            suffix = ".tif"
        elif tar_format == ".data2tiff":
            t_format = "data2tiff"
            suffix = ".tif"
        elif tar_format == ".data2tif":
            t_format = "data2tif"
            suffix = ".tif"
        elif tar_format == ".display2tiff":
            t_format = "display2tiff"
            suffix = ".tif"
        elif tar_format == ".display2tif":
            t_format = "display2tif"
            suffix = ".tif"
        return t_format, suffix

    def read_response(self):
        """读取响应"""
        response = rcf.recv_response()
        print(response)
        self.textEdit.insertPlainText(response)
        return response

    def start_convert(self):
        """开始转换"""
        self.is_start_convert = True
        self.start_format_convert_pushButton.setEnabled(False)
        self.stop_format_convert_pushButton.setEnabled(True)
        print("***开始转换***")

    def stop_convert(self):
        """结束转换"""
        self.is_start_convert = False
        self.start_format_convert_pushButton.setEnabled(True)
        self.stop_format_convert_pushButton.setEnabled(False)
        print("***结束转换***")

    def format_convert(self):
        """格式转换"""
        while True:
            print("等待转换...{}".format(self.is_start_convert))
            while self.is_start_convert:
                # print("开始转换...")
                try:
                    ori_format, tar_format = self.get_format()
                    print(self.all_list)
                    for file in self.all_list:
                        self.textEdit.insertPlainText("Start converting...\n")
                        try:
                            # 加载图像
                            self.str_cam_app.send_command_get_response("ImgLoad({},{})".format(ori_format[1:], file))
                            response = rcf.recv_response()
                            print(response)
                            self.textEdit.insertPlainText(response)
                            while response[0] != "0":
                                response = rcf.recv_response()
                                print(response)
                                self.textEdit.insertPlainText(response)
                            if response[0] == "0":
                                self.textEdit.insertPlainText("{}图像加载成功\n".format(file))
                                my_path = path.splitext(file)
                                t_format, suffix = self.get_target_format(tar_format)
                                out_filename = my_path[0] + suffix
                                # print("ImgSave(Current,{},{},0)".format(t_format, out_filename))

                                # 转换数据格式
                                self.str_cam_app.send_command_get_response(
                                    "ImgSave(Current,{},{},0)".format(t_format, out_filename))
                                response = rcf.recv_response()
                                print(response[0])
                                self.textEdit.insertPlainText(response)

                                while response[0] != "0":
                                    response = rcf.recv_response()
                                    print(response)
                                    self.textEdit.insertPlainText(response)
                                print(response[0])
                                if response[0] == "7":
                                    self.textEdit.insertPlainText("{}文件已经存在".format(out_filename))
                                    self.str_cam_app.send_command_get_response("ImgDelete(All)")
                                elif response[0] == "0":
                                    time.sleep(24)
                                    # 删除图片
                                    self.str_cam_app.send_command_get_response("ImgDelete(All)")
                                    response = rcf.recv_response()
                                    self.textEdit.insertPlainText(response)
                        except Exception as err:
                            self.textEdit.insertPlainText("{}".format(err))
                        self.all_list.remove(file)
                        self.all_tableWidget.removeRow(0)
                    self.stop_convert()
                except Exception as err:
                    print(err)
                time.sleep(1)
            time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = MainWindow()
    windows.show()
    sys.exit(app.exec_())
