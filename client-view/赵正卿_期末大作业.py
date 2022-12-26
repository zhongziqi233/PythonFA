from PyQt5.QtGui import *
from PyQt5.Qt import  *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import xml.dom.minidom
import sys


class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    x0_arr = []
    y0_arr = []
    x1_arr = []
    y1_arr = []
    flag = False

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    def mouseReleaseEvent(self, event):
        self.flag = False
        self.x0_arr.append(min(self.x0, self.x1))
        self.y0_arr.append(min(self.y0, self.y1))
        self.x1_arr.append(max(self.x0, self.x1))
        self.y1_arr.append(max(self.y0, self.y1))
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        x0 = min(self.x0, self.x1)
        y0 = min(self.y0, self.y1)
        x1 = max(self.x0, self.x1)
        y1 = max(self.y0, self.y1)
        width = x1 - x0
        height = y1 - y0

        rect = QRect(x0, y0, width, height)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)

        for i in range(len(self.x0_arr)):
            x = self.x0_arr[i]
            y = self.y0_arr[i]
            w = self.x1_arr[i] - self.x0_arr[i]
            h = self.y1_arr[i] - self.y0_arr[i]
            rect = QRect(x, y, w, h)
            painter.drawRect(rect)

class MainViewPort(QWidget):
    def __init__(self, Parent=None):
        super().__init__(Parent)
        self.resize(1000, 600)
        self.move(100, 50)
        self.setWindowTitle('标注工具')

        self.init_menuBar()
        self.init_sidebar()
        self.init_layout()

        self.lb = MyLabel(self)
        self.image_lo.addWidget(self.lb)

    def init_menuBar(self):
        self.menubar = QMenuBar(self)
        self.menubar.setFixedSize(QSize(1000, 25))
        self.fileMenu = self.menubar.addMenu('&文件')
        self.oprtMenu = self.menubar.addMenu('&操作')

        self.img_open_action = QAction('&打开图片', self)
        self.img_open_action.triggered.connect(self.img_open)
        self.fileMenu.addAction(self.img_open_action)

        self.xml_sav_action = QAction('&保存xml', self)
        self.xml_sav_action.triggered.connect(self.xml_save)
        self.fileMenu.addAction(self.xml_sav_action)

        self.undo_action = QAction('&撤销')
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setShortcut("Ctrl+Z")
        self.oprtMenu.addAction(self.undo_action)

    def init_sidebar(self):
        self.amount = 0

    def init_layout(self):
        self.main_lo = QHBoxLayout(self)
        self.main_lo.setSpacing(10)
        self.image_lo = QHBoxLayout()
        self.side_lo = QVBoxLayout()
        self.main_lo.addLayout(self.image_lo)
        self.main_lo.addLayout(self.side_lo)

    def img_open(self):
        formats = (["*.{}".format(format.data().decode("ascii").lower()) for format in QImageReader.supportedImageFormats()])
        fname = QFileDialog.getOpenFileName(self, "打开图片", "", "Image files ({})".format(" ".join(formats)))
        if not fname[0] == '':
            self.lb.setPixmap(QPixmap(fname[0]))
            self.lb.setFixedSize(QPixmap(fname[0]).size())
            self.lb.x0_arr = []
            self.lb.y0_arr = []
            self.lb.x1_arr = []
            self.lb.y1_arr = []

    def xml_save(self):
        x0_arr = self.lb.x0_arr
        y0_arr = self.lb.y0_arr
        x1_arr = self.lb.x1_arr
        y1_arr = self.lb.y1_arr
        name_arr = []
        if len(x0_arr) > 0:
            for i in range(self.amount):
                text = self.findChild(QLineEdit, 't' + str(i)).text()
                name_arr.append(text)
            mainDom = xml.dom.minidom.getDOMImplementation().createDocument(None, 'annotation', None)
            root = mainDom.documentElement
            for i in range(len(x0_arr)):
                obj = mainDom.createElement('object')
                root.appendChild(obj)

                if len(name_arr) - 1 < i:
                    name = 'unname' + str(len(name_arr) - 1 - i)
                else:
                    name = name_arr[i]
                nameE = mainDom.createElement('name')
                nameT = mainDom.createTextNode(name)
                nameE.appendChild(nameT)
                obj.appendChild(nameE)

                bndbox = mainDom.createElement('bndbox')
                obj.appendChild(bndbox)

                Ex0 = mainDom.createElement('xmin')
                Tx0 = mainDom.createTextNode(str(x0_arr[i]))
                Ex0.appendChild(Tx0)
                bndbox.appendChild(Ex0)

                Ey0 = mainDom.createElement('ymin')
                Ty0 = mainDom.createTextNode(str(y0_arr[i]))
                Ey0.appendChild(Ty0)
                bndbox.appendChild(Ey0)

                Ex1 = mainDom.createElement('xmax')
                Tx1 = mainDom.createTextNode(str(x1_arr[i]))
                Ex1.appendChild(Tx1)
                bndbox.appendChild(Ex1)

                Ey1 = mainDom.createElement('ymax')
                Ty1 = mainDom.createTextNode(str(y1_arr[i]))
                Ey1.appendChild(Ty1)
                bndbox.appendChild(Ey1)

            with open('annotation.xml', 'w', encoding='utf-8') as fs:
                mainDom.writexml(fs, addindent='    ', newl='\n')
                fs.close()

    def undo(self):
        if len(self.lb.x0_arr) != 0:
            self.lb.x0_arr.pop(len(self.lb.x0_arr) - 1)
            self.lb.y0_arr.pop(len(self.lb.y0_arr) - 1)
            self.lb.x1_arr.pop(len(self.lb.x1_arr) - 1)
            self.lb.y1_arr.pop(len(self.lb.y1_arr) - 1)
            self.update()

    def mouseReleaseEvent(self, event):
        self.update_sidebar()

    def update_sidebar(self):
        text = QLineEdit('unname' + str(self.amount))
        text.setObjectName('t' + str(self.amount))
        self.amount += 1
        self.side_lo.addWidget(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = MainViewPort()
    x.show()
    sys.exit(app.exec_())
