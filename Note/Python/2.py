# 菜单栏和工具栏
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget,\
        QAction, qApp, QMessageBox
from PyQt5.QtGui import QIcon

# 继承的QMainWindow类中包含经典的窗口结构
class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
        self.setGeometry(0, 0, 500, 500)
        self.setWindowTitle("PyQt5:状态栏、菜单栏、工具栏")
        self.center()

        # 状态栏显示信息
        self.statusBar().showMessage("空闲")

        # 先创建一个退出动作（exitAction）
        # QAction 创建一个抽象动作行为
        exitAction = QAction(QIcon("exit.jpg"), "&Exit", self)
        # 创建快捷键 +号左右两边不能有空格
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("点此退出程序！")
        # QAction“触发行为”信号连接到QApplication的quit
        exitAction.triggered.connect(qApp.quit)

        # 创建一个菜单栏 绑定退出动作
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(exitAction)

        # 创建一个工具栏 绑定退出动作
        self.toolBar = self.addToolBar("Exit")
        self.toolBar.addAction(exitAction)

        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "退出确认", "真的要退出么？",\
                QMessageBox.Yes|QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()




    def center(self):

        rec = self.frameGeometry()
        cent = QDesktopWidget().availableGeometry().center()
        rec.moveCenter(cent)
        self.move(rec.topLeft())


if __name__ == "__main__":

    app = QApplication(sys.argv)

    e = Example()

    sys.exit(app.exec_())
