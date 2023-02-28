from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QFileDialog,QPushButton,QComboBox,QLineEdit
import sys
import cv2
# model = YOLO('yolov8s.pt')
from PyQt5.QtGui import QImage

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5 import QtGui
from ultralytics import YOLO
from screeninfo import get_monitors

model = YOLO('yolov8s.pt')



class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.password = QLineEdit()
        self.backg = QLabel()
        self.im = QPixmap("./3.jpg")
        self.label = QLabel()
        self.backg.setPixmap(self.im)

        self.password.setEchoMode(QLineEdit.Password)

        self.button2 = QPushButton()
        self.button2.setText("Start")
        # self.button2.move(64,64)

        self.button2.clicked.connect(self.button2_clicked)

        self.grid.addWidget(self.password, 2,1)
        self.grid.addWidget(self.button2,2,2)

        self.grid.addWidget(self.backg,1,1, 1, 2)



        self.setLayout(self.grid)
        self.setGeometry(600,150,400,300)
        self.setWindowTitle("PyQT show image")
        self.show()
        for m in get_monitors():
            # print(str(m))
            str1 = str(m)
            self.width = int(str1[24:28])
            self.height = int(str1[37:41])
            # print('width',str1[24:28])
            # print('height', str1[37:41])
            # print('width_mm', str1[52:55])
            # print('height_mm', str1[67:71])
    def button2_clicked(self):
        passwor = self.password.text()
        if passwor == 'doctor':
            self.w = Example()
            self.w.show()
            self.hide()
        else:
            print('Wrong')
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('wind')


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.button1 = QPushButton()
        self.button1.setText("Browser...")
        self.button1.setFont(QFont('Times', 15))
        # self.button1.move(64,32)
        self.button1.clicked.connect(self.button1_clicked)

        self.button2 = QPushButton()
        self.button2.setFont(QFont('Times', 15))
        self.button2.setText("Exit")
        # self.button2.move(64,64)

        self.button2.clicked.connect(self.button2_clicked)

        self.label = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()
        self.label4 = QLabel()
        
        self.label.setFont(QFont('Arial', 20))
        self.label2.setFont(QFont('Arial', 20))
        self.label3.setFont(QFont('Arial', 20))
        self.label4.setFont(QFont('Arial', 20))
        
        self.combo = QComboBox()
        self.combo.addItem("800*600")
        self.combo.addItem("1000*800")
        self.combo.addItem("1200*900")
        self.combo.setFont(QFont('Times', 15))

        self.combo.activated[str].connect(self.onChanged)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label,1,1,1,2)
        self.grid.addWidget(self.button1, 5,1)
        # self.grid.addWidget(self.table, 3,1)
        self.grid.addWidget(self.button2, 5,2)
        self.grid.addWidget(self.combo, 3,1, 1, 2)
        self.grid.addWidget(self.label2,2,1)
        self.grid.addWidget(self.label3,2,2)
        # self.grid.addWidget(self.label4,7,1)
        self.setLayout(self.grid)

        self.setGeometry(600,150,1000,800)
        self.img_width = 900
        self.img_height = 700
        self.setWindowTitle("PyQT show image")
        self.show()

    def onChanged(self, text):
        if text == '800*600':
            self.setGeometry(600,150,800,600)
            self.img_width = 700
            self.img_height = 500
        elif text =='1000*800':
            self.setGeometry(600,150,1000,800)
            self.img_width = 900
            self.img_height = 700
        elif text =='1200*900':
            self.setGeometry(600,150,1200,900)
            self.img_width = 1100
            self.img_height = 800

    def button1_clicked(self):
        self.source_path , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                "", "All Files (*);;Python Files (*.mp4);;Text Files (*.jpg)")
        if check:
            self.cap = cv2.VideoCapture(self.source_path)
            while(self.cap.isOpened()):
                ret, frame = self.cap.read()
                frame = cv2.resize(frame, (self.img_width, self.img_height))
                if ret == False:
                    break
                results = model.predict(source=frame,conf=0.5)

                for r in results:
                    self.name = ''
                    class_name = []
                    for c in r.boxes.cls:
                        self.name = self.name + '\n' + model.names[int(c)]
                        self.label2.setText(self.name)
                        class_name.append(model.names[int(c)])

                    conf = r.boxes.conf
                    conf1 =conf.tolist()
                    if conf1 is not None:
                        self.percept=''
                        for confs in conf1:
                            conf_str = str(confs)
                            self.percept = self.percept + '\n' + conf_str[1:8] +'%'
                            self.label3.setText(self.percept)

                    tensor_pos = r.boxes.xyxy
                    list_pos = tensor_pos.tolist()
                    if list_pos is not None:
                        i = 0
                        for pos in list_pos:
                            print(class_name[i])
                            font = cv2.FONT_HERSHEY_SIMPLEX

                            cv2.rectangle(frame, (int(pos[0]), int(pos[1])), (int(pos[2]), int(pos[3])), (255, 255, 0), 2)
                            # image = cv2.putText(frame, class_name[], org, font, 1,  (123, 344, 321), 4, cv2.LINE_AA, False)
                            # cv2.putText(frame, class_name[i], (int(pos[0]), int(pos[1])),  (0, 255, 0), 2)
                            cv2.putText(frame, class_name[i],  (int(pos[0]), int(pos[1])) ,cv2.FONT_HERSHEY_SIMPLEX,  1,(255,0 , 255, 255),  1)
                            i += 1
                image = frame
                image1 = QImage(image, image.shape[1],image.shape[0],image.strides[0],QImage.Format_RGB888)
                self.label.setPixmap(QtGui.QPixmap.fromImage(image1))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            self.cap.release()

    def button2_clicked(self):
        sys.exit(app.exec_())
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    sys.exit(app.exec_())
