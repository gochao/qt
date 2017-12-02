# Widgets(1):复选按钮（QCheckBox），切换按钮（ToggleButton），滑块条（QSlider）
# 进度条（ProgressBar）和日历组件（QCalendarWidget）
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox,\
    QPushButton, QFrame, QSlider, QProgressBar, QCalendarWidget,\
    QLabel
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtCore import Qt, QBasicTimer, QDate


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.col = QColor(0, 0, 0)
        self.ui()

    def ui(self):
        # checkbox
        mycheckbox = QCheckBox("Change-Title", self)
        mycheckbox.toggle()
        mycheckbox.move(50, 50)
        mycheckbox.stateChanged.connect(self.changetitle)

        # toggle button(QPushbutton)
        red_toggle = QPushButton("Red", self)
        red_toggle.move(50, 100)
        red_toggle.setCheckable(True)
        red_toggle.clicked[bool].connect(self.set_color)

        green_toggle = QPushButton("Green", self)
        green_toggle.move(50, 150)
        green_toggle.setCheckable(True)
        green_toggle.clicked[bool].connect(self.set_color)

        blue_toggle = QPushButton("Blue", self)
        blue_toggle.move(50, 200)
        blue_toggle.setCheckable(True)
        blue_toggle.clicked[bool].connect(self.set_color)

        self.color_frame = QFrame(self)
        self.color_frame.setGeometry(150, 100, 150, 120)
        self.color_frame.setStyleSheet("QWidget{background-color:%s}" % self.col.name())

        # QSlider
        red_slider = QSlider(Qt.Horizontal, self)
        red_slider.setFocusPolicy(Qt.NoFocus)
        red_slider.setGeometry(50, 250, 250, 20)
        red_slider.valueChanged[int].connect(self.change_value)

        green_slider = QSlider(Qt.Horizontal, self)
        green_slider.setFocusPolicy(Qt.NoFocus)
        green_slider.setGeometry(50, 270, 250, 20)
        green_slider.valueChanged[int].connect(self.change_value)

        blue_slider = QSlider(Qt.Horizontal, self)
        blue_slider.setFocusPolicy(Qt.NoFocus)
        blue_slider.setGeometry(50, 290, 250, 20)
        blue_slider.valueChanged[int].connect(self.change_value)

        # ProgressBar
        self.pbr = QProgressBar(self)
        self.pbr.setGeometry(50, 320, 250, 20)

        self.pbrbtn = QPushButton("start", self)
        self.pbrbtn.move(150, 350)
        self.pbrbtn.clicked.connect(self.progressbar)

        self.timer = QBasicTimer()
        self.step = 0

        # QCalendarWidget
        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(50, 420)
        cal.clicked[QDate].connect(self.showdate)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())
        self.lbl.move(100, 400)

        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle("Widgets")
        self.show()

    def changetitle(self, state):
        if state:
            self.setWindowTitle("Check-box:selecked")
        else:
            self.setWindowTitle("Check-box:not-selecked")

    def set_color(self, state):
        sender_name = self.sender().text()
        if state:
            val = 255
        else:
            val = 0

        if sender_name == "Red":
            self.col.setRed(val)
        elif sender_name == "Green":
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)

        self.color_frame.setStyleSheet("QWidget{background-color:%s}"%self.col.name())

    def change_value(self, value):
        sender_name = self.sender()
        val = value/100 * 255
        if sender_name == "red_slider":
            self.col.setRed(val)
        elif sender_name == "green_slider":
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)
        self.color_frame.setStyleSheet("QWidget{background-color:%s}"%self.col.name())

    def timerEvent(self, QTimerEvent):
        if self.step >= 100:
            self.timer.stop()
            self.pbrbtn.setText("Finished")
            return
        self.step += 1
        self.pbr.setValue(self.step)

    def progressbar(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pbrbtn.setText("Start")
        else:
            self.timer.start(100, self)
            self.pbrbtn.setText("Stop")

    def showdate(self, date):
        self.lbl.setText(date.toString())

if __name__ =="__main__":
    app = QApplication(sys.argv)

    e = Example()

    sys.exit(app.exec())