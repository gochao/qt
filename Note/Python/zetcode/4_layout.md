# 布局管理

GUI程序的布局管理是一个很重要的方面  
布局管理是我们如何在应用上放置组件  
布局管理有两种基本的方式,绝对位置或布局类

# 绝对位置  
程序员确定每个组件的尺寸和位置,当你使用绝对布局时,考虑以下限制:  
1. 改变窗口大小时,组件的位置不会变
2. 改变应用字体时,可能会损坏布局  
3. 应用在不同平台看起来会不一样  
4. 如果我们决定更改布局,那么我们就必须全部调整,非常耗时  

```
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



## 箱式布局  
用布局类来布局管理会更灵活实际,在它是更常用的方式  
QHBoxLayout(水平)和QVBOXLayout(竖直)是基础的布局类  

想像我们放置两个按钮在右下角  
为了制造这样的布局,我们使用一个水平和竖直箱  
为了留出必要的空间,我们添加一个拉伸因子  

```
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


## 网格布局  
最通用的布局类是网格布局,这种布局将空间按行和列拆分  
为了创建网格布局,我们使用QGridLayout类 

```
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


# 跨多行放置部件  
网格布局可以划分多行和列,组件可以占多行列  

```
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