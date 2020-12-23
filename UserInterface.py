import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot, QCoreApplication, QThread
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import time

import imageio


def input_classname(class_name):
    res = []
    for folder in os.listdir("/Users/moon/DataCapston/yolo_object_detection/output2/"+class_name+"/"):
        res.append("/Users/moon/DataCapston/yolo_object_detection/output2/"+class_name+"/"+folder)
    # print (res)
    return res
# input_classname("handbag")



class Ui_Main(QWidget):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(0, 0)
        self.stack1 = QWidget()
        self.stack2 = QWidget()

        uic.loadUi("DC1.ui", self.stack1)
        uic.loadUi("DC2.ui", self.stack2)

        self.QtStack = QStackedLayout(self)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)



class Main(QMainWindow, Ui_Main):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.class_inputname = ""
        self.setupUi(self)
        self.top1_imagelist=[]
        self.top2_imagelist=[]
        self.top3_imagelist=[]

        self.stack1.textEdit.setStyleSheet('QTextEdit {font-size:24pt; color: #323232;}')
        self.stack2.motion_name.setStyleSheet('QTextBrowser {font-size:24pt; color: #323232;}')
        self.stack2.Top1.setStyleSheet('QTextBrowser {font-size:12pt; color: #323232;}')
        self.stack2.Top2.setStyleSheet('QTextBrowser {font-size:12pt; color: #323232;}')
        self.stack2.Top3.setStyleSheet('QTextBrowser {font-size:12pt; color: #323232;}')

        self.stack1.search_button.clicked.connect(self.OpenWindow)
        self.stack2.back_button.clicked.connect(self.BackWindow)
        self.stack2.quit_Button.clicked.connect(self.QuitWindow)
        self.stack2.Top1pushButton.clicked.connect(self.videoplay)
        self.stack2.Top2pushButton.clicked.connect(self.videoplay2)
        self.stack2.Top3pushButton.clicked.connect(self.videoplay3)

    def OpenWindow(self):
        self.class_inputname = self.stack1.textEdit.toPlainText()
        # if (self.class_inputname == ""):
        #     self.stack1.textEdit.setText("객체를 넣어주세요")
        #     self.stack1.textEdit.setStyleSheet('QTextEdit {background-color: #E7E7E7; color: #E05263;}')
        #     #             self.stack1.filename.setAlignment(Qt.AlignCenter)
        #     return
        self.QtStack.setCurrentIndex(1)
        res = input_classname(self.class_inputname)

        self.stack2.motion_name.setPlainText(self.class_inputname)
        self.stack2.Top1.setPlainText(res[0][len(res[0])-1])
        self.stack2.Top2.setPlainText(res[1][len(res[1])-1])
        self.stack2.Top3.setPlainText(res[2][len(res[2])-1])
        for dir in os.listdir(res[0]):
            self.top1_imagelist.append(res[0]+"/"+dir)
        for dir in os.listdir(res[1]):
            self.top2_imagelist.append(res[1]+"/"+dir)
        for dir in os.listdir(res[2]):
            self.top3_imagelist.append(res[2]+"/"+dir)

        self.input_classname = ""

    def BackWindow(self):
        self.QtStack.setCurrentIndex(0)

    def QuitWindow(self):
        app.quit()

    def videoplay(self):
        images=[]
        for filename in self.top1_imagelist:
            images.append(imageio.imread(filename))
        imageio.mimsave('/Users/moon/DataCapston/movie.gif', images)

        self.movie = QMovie("/Users/moon/DataCapston/movie.gif")
        self.stack2.display_label.setMovie(self.movie)
        self.stack2.display_label.setScaledContents(True)
        self.movie.start()
    def videoplay2(self):
        images=[]
        for filename in self.top2_imagelist:
            images.append(imageio.imread(filename))
        imageio.mimsave('/Users/moon/DataCapston/movie.gif', images)

        self.movie = QMovie("/Users/moon/DataCapston/movie.gif")
        self.stack2.display_label.setMovie(self.movie)
        self.stack2.display_label.setScaledContents(True)
        self.movie.start()
    def videoplay3(self):
        images=[]
        for filename in self.top3_imagelist:
            images.append(imageio.imread(filename))
        imageio.mimsave('/Users/moon/DataCapston/movie.gif', images)

        self.movie = QMovie("/Users/moon/DataCapston/movie.gif")
        self.stack2.display_label.setMovie(self.movie)
        self.stack2.display_label.setScaledContents(True)
        self.movie.start()


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = Main()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()



    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()