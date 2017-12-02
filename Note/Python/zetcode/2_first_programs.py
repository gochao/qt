import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, \
    QPushButton, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import  QCoreApplication


def example1():

    # 每个应用都要创造一个应用对象,sys.argv参数是命令行的参数列表
    app = QApplication(sys.argv)

    # QWidget是所有实例对象的基础类
    # 我们创建的是默认构造函数,没有parent
    # 没有父亲(parent)的组件被称作窗口(window)
    w = QWidget()

    # 宽250, 高150像素
    w.resize(250, 150)

    # 将组件移动
    w.move(300, 300)

    # w是一个窗口,此时设置窗口名称
    w.setWindowTitle('Simple')

    # 显示在屏幕上,组件会先被创建在内存中,之后显示在屏幕上
    w.show()

    # 最后我们进入应用循环中,时间处理从此时开始,主循环接受从窗口系统传来的事件
    # 并调度应用组件,我们调用exit()函数后,主循环结束,组件被消除
    # sys.exit()方法保证了一个干净的退出
    # 环境将被告知应用如何结束
    # exec_()方法,有下划线是因为exec是python的关键字
    sys.exit(app.exec_())


# 之前的例子是一个面向过程,Python支持面向过程,以及面向对象
# 创建一个新的类Example,这个类继承自QWidget类
# 两个构造方法,super()方法返回父类对象
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置屏幕位置和设置大小
        self.setGeometry(300, 300, 1000, 200)
        self.setWindowTitle('Icon')
        # 设置图标,要用QIcon创建一个图标对象
        self.setWindowIcon(QIcon('web.png'))

        self.show()



# 显示气泡提示QToolTip
class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置提示气泡的字体大小
        QToolTip.setFont(QFont('SansSerif', 10))
        # 给窗口设置提示
        self.setToolTip('this is a <b>QWidget</b> widget')

        # 创建一个按钮并加上提示
        btn = QPushButton('按钮', self)
        btn.setToolTip('this is a <b>QPushButton</b> widget')

        # 按钮大小设置为推荐大小
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        self.setGeometry(300, 300, 1000, 200)
        self.setWindowTitle('Tooltips')
        self.show()



# 关闭窗口
# 大多部件都有父母,没有父母的部件是顶级窗口
# 点击x
class Example3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 参数1:按钮上的文字, 参数2:该按钮的父亲
        btn = QPushButton('点我退出', self)

        # 信号-槽机制
        # 如果点击按钮,信号clicked会被发出,槽可以是Qt的槽,也可以是Python的可调用对象
        # QCoreApplication 包含主事件循环,它是由QApplication创建的,负责处理和调度所有事件
        # instance()给我们当前的实例
        # 点击信号,连接到终止应用程序的quit()方法,发件人是按钮,收件人是应用对象
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.resize(btn.sizeHint())
        btn.move(0, 0)

        self.setGeometry(300, 300, 1000, 100)
        self.setWindowTitle('quit')
        self.show()


# 消息提示框
# 默认下,我们点击关闭的X,就关闭窗口了
# 有时我们需要调整默认的行为
# 例如,如果我们有一个编辑过的文件,关闭时需要提醒保存
class Example4(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Message box')
        self.show()

    # 我们关闭QWidget时,会触发QCloseEvent事件
    # 重写QWidget的关闭事件,能够改变关闭行为
    def closeEvent(self, QCloseEvent):
        # self, 标题, 信息内容,按钮,默认按钮焦点
        reply = QMessageBox.question(self, "Messagee",
                                     "真的离开?", QMessageBox.Yes | QMessageBox.No,\
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


# 将窗口移动到屏幕中心
class Example5(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(1000, 200)
        self.center()

        self.setWindowTitle("Center")
        self.show()

    def center(self):
        # 获得一个矩形,其大小与主窗口一致
        qr = self.frameGeometry()

        # QDesktopWidget提供用户屏幕的信息,拿到屏幕的中心点
        cp = QDesktopWidget().availableGeometry().center()

        # qr矩形中心移动到屏幕中心cp
        qr.moveCenter(cp)

        # 将主窗口的定位点(左上角)移动到矩形的左上角点
        self.move(qr.topLeft())



if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = Example5()
    sys.exit(app.exec_())


