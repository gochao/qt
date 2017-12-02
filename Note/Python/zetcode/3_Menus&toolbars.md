# Menus and toolbars in PyQt5

这部分教程中,我们将制造一个菜单和工具栏  
菜单是在菜单栏的一组命令  
工具栏是应用中的一些常见按钮  

## 主窗口  
QMainWindow类提供了一个主应用窗口类,是一个具有状态栏,工具栏,菜单栏的框架  
之前我们用的主窗口都是QWidget类  


## 状态栏  
状态栏是一个显示状态的组件  
```
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


## 菜单栏
菜单栏是一个GUI应用的公共部分,它是一组菜单命令
```
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


## 工具栏  
菜单栏包含了所有应用中我们可以用的命令,工具栏是快速调用我们常用的命令  

```
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
