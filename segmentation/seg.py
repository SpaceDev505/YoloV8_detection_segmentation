from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QFileDialog,QPushButton,QComboBox,QLineEdit
import sys
import cv2
# model = YOLO('yolov8s.pt')
from PyQt5.QtGui import QImage

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *
from PyQt5 import QtGui
from ultralytics import YOLO
from yoloseg import YOLOSeg

# model = YOLO('yolov8s.pt')

model_path = "./yolov8s-seg.onnx"
yoloseg = YOLOSeg(model_path, conf_thres=0.3, iou_thres=0.3)
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
        # self.button1.move(64,32)
        self.button1.clicked.connect(self.button1_clicked)

        self.button2 = QPushButton()
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
        self.combo.activated[str].connect(self.onChanged)

        self.grid = QGridLayout()
        self.grid.addWidget(self.label,1,1,1,2)
        self.grid.addWidget(self.button1, 5,1)
        # self.grid.addWidget(self.table, 3,1)
        self.grid.addWidget(self.button2, 5,2)
        self.grid.addWidget(self.combo, 3,1,1,2)
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

                if not ret:
                    break

                # Update object localizer
                boxes, scores, class_ids, masks = yoloseg(frame)

                combined_img = yoloseg.draw_masks(frame)
                # cv2.imshow("Detected Objects", combined_img)

                image = combined_img
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
