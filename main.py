import os
import sys
from PyQt5.Qt import  *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class myMainWindow(QWidget):
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.setWindowTitle('目标检测数据集标注工具')
        self.setFixedSize(1500, 900)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = myMainWindow()
    form.show()
    exit(app.exec_())