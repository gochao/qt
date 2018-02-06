# PyQt 学习笔记

资料来源:[zetcode](http://zetcode.com/gui/pyqt5/)

[TOC]

## PyQt5介绍  

这是PyQt5教程的介绍,目的是让你开始使用PyQt5工具箱.教程已经在linux上完成并测试.

### 关于PyQt5

PyQt5是一系列Qt5绑定在Python上的应用框架,它可以在2.x和3.x上使用  

本教程使用Python3    
包含620个类,6000个函数和方法  

类被分为以下模块:  

- QtCore
- QtGui
- QtWidgets
- QtMultimedia
- QtBluetooth
- QtNetwork
- QtPositioning
- Enginio
- QtWebSockets
- QtWebKit
- QtWebKitWidgets
- QtXml
- QtSvg
- QtSql
- QtTest

QtCore模块包含了非GUI功能,这个模块用于:  
时间,文件,字典,变量数据类型,流,URLS,mime类型,线程或进程.  

QtGUI模块:  
包含了窗口系统,事件处理,2D图像,基础绘图,字体和文字  

QtWidgets模块:  
提供一系列UI事件来创建桌面类型的用户接口  

QtMultimedia模块:  
处理多媒体内容,和API访问摄像头和音频  

QtBluetooth模块:
包含从设备和链接中获取内容的类  

QtNetwork模块:  
网络程序,TCP/IP和UDP客户端于服务更加简单  

QtPositioning:  
决定位置,卫星,Wifi,或文本本件  

Enginio模块:
解决客户端访问Qt云服务托管


---

## 简单的例子  
显示一个小窗口,之后可以实现更多功能.  
重新设置大小需要很多代码,一些人已经写好了函数,因为他们在很多应用中重复  
因此不需要在写了  
PyQt5是一个高级的工具箱,如果我们写了低级的代码,接下来的这个例子就会轻松上百行  

### 代码示例

```py
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

    def initUI(self)
```

---
## 菜单栏工具栏

这部分教程中,我们将制造一个菜单和工具栏  
菜单是在菜单栏的一组命令  
工具栏是应用中的一些常见按钮  

### 主窗口  
QMainWindow类提供了一个主应用窗口类,是一个具有状态栏,工具栏,菜单栏的框架  
之前我们用的主窗口都是QWidget类  

### 状态栏  

状态栏是一个显示状态的组件  

```py
# 继承的类是QMainWindow,包含状态栏,菜单栏,工具栏
class Example1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # 设置状态栏信息
        # 状态栏提示是对组件的说明或帮助
        # 第一次调用状态栏是会创建
        self.statusBar().showMessage("Ready")

        self.setGeometry(300, 300, 1000, 200)
        self.setWindowTitle("statusbar")
        self.show()
```


### 菜单栏

菜单栏是一个GUI应用的公共部分,它是一组菜单命令  

```py
# 菜单栏
# 菜单栏里有一个file菜单
# file菜单里有有一个exit_action的QAction
# 这个QAcion有图标,有快捷键,和状态栏说明
class Example2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # 创建一个退出动作,赋予图标,快捷键,状态说明
        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip("退出")
        # 动作触发信号,连接到退出槽
        exit_action.triggered.connect(qApp.quit)

        # 调用状态栏,使它创建
        self.statusBar()

        # 在菜单栏创建一个菜单
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exit_action)

        self.setGeometry(300,300, 1000, 200)
        self.show()
```


### 工具栏

菜单栏包含了所有应用中我们可以用的命令,工具栏是快速调用我们常用的命令  

```py
class Example3(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建一个退出动作,赋予图标,快捷键,状态说明
        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip("退出")
        # 动作触发信号,连接到退出槽
        exit_action.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('tuichu')
        self.toolbar.addAction(exit_action)


        self.setGeometry(300, 300, 1000, 200)
        self.show()
```

---
## 布局管理

GUI程序的布局管理是一个很重要的方面  
布局管理是我们如何在应用上放置组件  
布局管理有两种基本的方式,绝对位置或布局类  

### 绝对位置
程序员确定每个组件的尺寸和位置,当你使用绝对布局时,考虑以下限制:  
- 改变窗口大小时,组件的位置不会变
- 改变应用字体时,可能会损坏布局  
- 应用在不同平台看起来会不一样  
- 如果我们决定更改布局,那么我们就必须全部调整,非常耗时  

```py
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl1 = QLabel('zetcode', self)
        lbl1.move(0,0)

        lbl2 = QLabel('tutorials', self)
        lbl2.move(35, 40)

        lbl3 = QLabel('for', self)
        lbl3.move(80, 80)


        self.setGeometry(300, 300, 1000, 300)
        self.show()
```

### 箱式布局

用布局类来布局管理会更灵活实际,在它是更常用的方式  
QHBoxLayout(水平)和QVBOXLayout(竖直)是基础的布局类  

想像我们放置两个按钮在右下角  
为了制造这样的布局,我们使用一个水平和竖直箱  
为了留出必要的空间,我们添加一个拉伸因子  

```py
class Example2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建两个按钮
        ok_btn = QPushButton("OK")
        cancle_btn = QPushButton("Cancel")

        # 创建水平布局,添加拉伸因子,将两个按钮加进去
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancle_btn)

        # 创建竖直布局,将水平布局放入
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        # 设置主窗口布局
        self.setLayout(vbox)

        self.setGeometry(300, 300, 1000, 300)
        self.show()
```

### 网格布局

最通用的布局类是网格布局,这种布局将空间按行和列拆分  
为了创建网格布局,我们使用QGridLayout类  

```py
class Example3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']
        positions = [(i, j) for i in range(5) for j in range(4)]

        for position,name in zip(positions, names):
            if name == "":
                continue
            button = QPushButton(name)
            grid.addWidget(button, position[0], position[1])

        self.setGeometry(300, 300, 400, 400)
        self.show()
```

### 跨多行放置部件

网格布局可以划分多行和列,组件可以占多行列  

```py
class Example4(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        title = QLabel("Title")
        author = QLabel("Author")
        review = QLabel("Review")

        title_edit = QLineEdit()
        author_edit = QLineEdit()
        review_edit = QTextEdit()

        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(title_edit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(author_edit, 2, 1)

        grid.addWidget(review, 3, 0)
        # 从第三行到第五行
        grid.addWidget(review_edit, 3, 1, 15, 1)

        self.setGeometry(300, 300, 400, 400)
        self.show()
```