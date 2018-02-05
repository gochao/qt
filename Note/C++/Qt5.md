# [《Qt5 学习之路2》](https://www.devbean.net/)

[TOC]
---  
## Hello World  

### 新建项目

1. 打开Qt Creator
2. 新建工程-Application-GUI应用  
3. 编译器选择mingw调试  
4. shadow build是将构建生成的文件不放在源码文件夹下，保持整洁  
5. 不选中创建界面

创建完成后文件夹下有：  
1. main.cpp：包含main函数    
2. mainwindow.cpp  
3. mainwindow.h  
4. HelloWorld.pro：QT工程文件，包含引入的类，qt版本号，目标程序名，源代码文件和头文件名


### 编写main.cpp 

```cpp
//引入类
#include <QApplication>
#include <QLabel>

int main(int argc, char *argv[])
{
    //创建QApplication类的实例
    //用于管理程序生命周期开启事件循环
    QApplication app(argc, argv);

    //创建标签，文本内容为“Hello world”
    QLabel label("Hello world");
    
    //显示标签
    label.show();
    
    //开启事件循环，如果没有循环，main函数此时就执行完毕自动退出
    return app.exec();
}
```

修改后点左侧下方的绿色按钮运行  


---
## 信号槽机制  

1. 信号槽机制就是观察者模式,当发生了感兴趣的事件，某一个操作就会被自动触发  
2. 当事件发生时，被观察对象会发出一个信号。这个信号没有目的，类似广播信号  
3. 如果存在一个观察者在观察该对象，它对这个信号感兴趣，那么就会连接（connect）这个信号，用自己的槽函数（slot）来处理这个信号  
4. 当信号发出时，与该信号连接的槽函数会被调用  

### 信号槽举例

```cpp
#include <QApplication>
#include <QPushButton>

int main(int argc, char *argv[])  
{
    QApplication app(argc, argv);
    //创建文本为Quit的按钮
    QPushButton button("Quit");
    
    //将这个按钮的“clicked”信号连接到app.quit函数上
    //即当按钮被按下时，发出clicked信号，由connect链接到槽函数app.quit，程序退出
    QObject::connect(&button, &QPushButton::clicked, &QApplication::quit);
    
    button.show();

    return app.exec();
}
```


### connect函数

该函数有五个重载  
常用形式：

```cpp
//sender对象发送signal后，自动调用recevier的slot函数
QObject::connect(sender, signal, receiver, slot);
```

在上面的例子中，connect只有三个参数，缺少了recevier  
使用的就是重载之一，receiver默认为this  


### 参数问题
1. 信号参数与槽函数参数一致  
2. 允许槽函数的参数比信号参数少，槽函数可以选择性的忽略一部分信号  
3. 但是信号中不存在的信息，槽函数不能无中生有  


### 信号链接到Lambda表达式  

```cpp
#include <QApplication>
#include <QPushButton>
#include <QDebug>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QPushbutton button("Quit");
    //槽函数的函数是一个Lambda表达式，接受一个bool参数，输出一个字符串
    //qDebug类似cout，若编译该函数需要在pro文件中添加配置
    Qobject::connect(&button, &QPushButton::clicked, [](bool){qDebug() << "clicked!!";});
    button.show();

    return app.exec();
}
```

### C++的Lambda表达式  

```cpp
[capture](parameters)opt->ret{body}

[]内为接受的外部参数  
()内为定义的内部参数  
opt选填mutable exception attribute  
ret返回值类型  
body函数体  
```


## 自定义信号槽  

我们可以自己设计信号和槽，用于解耦  

### 观察者模式  

1. 存在报纸订阅者（观察者）和报纸（被观察者）  
2. 当被观察者（报纸）有了新内容时会通知观察者（用户）  
3. 观察者（用户）一般会注册在被观察者（报纸机构）的容器内，当发生变化时，被观察者会主动遍历这个容器，依次通知各个观察者（用户）  


### 举例
例子代码包含三个文件：  
1. main.cpp
2. newsPaper.h
3. reader.h

#### main.cpp

创建订阅者和报纸对象，连接信号-槽实现观察者模式

```cpp
#include <QCoreApplication>
#include "newspaper.h"
#include "reader.h"

int main(int argc, char *argv[])
    QCoreApplication app(argc, argv);

    Newspaper newspaper("Newspaper A");
    Reader reader;

    QObject::connect(&newspaper, &Newspaper::newPaper, &reader, &Reader::receiveNewspaper);
    
    newspaper.send();

    return app.exec();
```

#### newsPaper.h

被观察者发送信号  

```cpp
#include <QObject>

// Newspaper类继承QObject，才有信号槽能力
class Newspaper : public QObject
{
    //QObject类都要有这个宏，被moc预处理 
    Q_OBJECT  

public:
    Newspaper(const QString &name): m_name(name)
    {
    }

    //执行该函数时出发自身的信号
    void send()
    {
        emit newPaper(m_name); // 发信号
    }

private:
    QString m_name;

//定义了信号
signals:
    void newPaper(const QString &name);
};
```

#### reader.h

读者为观察者，在接受到信号时，处理自己的槽函数

```cpp
#include <QObject>
#include <QDebug>

class Reader : public QObject
{
    //继承QObject必需的语句
    Q_OBJECT

public:
    //构造函数
    Reader(){} 

    //槽函数
    void receiveNewspaper(const QString & name)
    {
        qDebug() << "Receives Newspaper:" << name;
    }
};
```


### 注意事项

* 发送者和接收者都要是QObject的子类，只用继承了QObject类，才有信号槽的能力  
* 继承了QObject类的子类，第一行代码都要写上Q_OBJECT宏，这个宏的展开能够提供为类提供信号槽机制以及其它操作  
* 使用signals标记信号函数，信号只是一个函数声明，返回void（只需发出即可），不需要实现代码    
* 槽函数可以是任何成员函数，static函数，全局函数和Lambda表达式。它也会受到public，private，protected影响  
* emit发送信号 
* QObject::connect（） 连接信号和槽  


---
## MainWindow 简介  

QMainWindow是一个预定义好的一个主窗口类，是应用程序最顶层的窗口  
标题栏，菜单栏，工具栏，任务栏  

```cpp
#include "mainwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    MainWindow win;
    win.show();

    return app.exec();
}
```

* 标题栏（Title）：显示标题和控制按钮（最大小化+关闭）  
* 菜单栏（Menu Bar）：显示菜单  
* 状态栏（Status Bar）：鼠标划过，下方会有文字提示  


### pro文件  

- 定义QT，告诉编译器需要使用哪些模块，通常需要加入core，gui  
- 第二行：Qt的主版本号和添加的widgets  
- TARGET是生成程序的名字  
- TEMPLATE是生成makefile所使用的模板  
- SOURCES和HEADERS是项目所需要的源代码文件和头文件  


---
## 菜单栏 工具栏 状态栏  

将用户与界面进行交互的元素抽象成一种动作，使用QAction类表示  
QAction可以添加到菜单栏，工具栏和状态栏上  

开发中，QMainWindow作为主窗口  
QDialog作为对话框窗口  

### 菜单栏

`menuBar()`函数由QMainWindow提供，用于返回窗口的菜单栏（如果有）  
如果没有就创建一个菜单栏  

QMenuBar类，代表窗口最上方的一条菜单栏  
addMenu()可以添加菜单  
&符号为菜单创建一个快捷键  
创建出菜单对象时，可以把QAction添加到这个菜单上面（addAction）  


### 工具栏  

QToolBar 工具栏类  
`addToolBar()`新加一个工具栏，而菜单栏则是`menuBar()`，这是因为一个窗口只有一个菜单栏，但可以有多个工具栏  
工具栏可以设置成固定的，浮动的  


### 状态栏  

`statusBar()`返回状态栏  
QAction::setStatusTip()可以设置某动作在状态栏上的提示文本  


---
## QAction添加动作   

QAction类为动作类  
它能够完成窗口的动作，如显示菜单；对用户的点击做出响应  
Qt没有专门的**菜单项**类，它用QAction类抽象出公共动作，添加到菜单就是菜单项，添加到工具栏就是工具按钮  
包含：图标，菜单文字，快捷键，状态栏文字，浮动帮助等信息，QACtion对象加到程序中时，Qt自己选择使用哪个属性来显示  

### 使用举例

#### main.cpp 

```cpp
#include "mainwindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    MainWindow win;
    win.show();

    return app.exec();
}
```

#### mainwindow.h 

```cpp
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    //构建一个私有函数open
    void open();

    //构建一个私有变量openAction
    QAction *openAction;
};

#endif
```

#### mainwindow.cpp

```cpp
#include <QAction>
#include <QMenuBar>
#include <QMessageBox>
#include <QStatusBar>
#include <QToolBar>

#include "mainwindow.h"

//MainWindow的构造函数
MainWindow::MainWindow(QWidget *parent): QMainWindow(parent)
{
    
    //设置窗口标题,tr()函数用于国际化
    setWindowTitle(tr("主窗口"));

    //创建openAction对象
    //第一个参数还可以加入图标图像(此处未加),第二个参数中有&,意味着是一个快捷键
    openAction = new QAction(tr("&打开文件"), this);

    //设置快捷键，这里的快捷键用的是内置通用的快捷键Open
    //也可以设置tr("Ctrl+O")来设置快捷键
    //但设置通用的快捷键，跨平台较为方便
    openAction->setShortcuts(QKeySequence::Open);
    //设置状态栏的信息
    openAction->setStatusTip(tr("点击打开文件"));

    //openAction触发信号与MainWindow类的open()函数连接
    connect(openAction, &QAction::triggered, this, &MainWindow::open);

    //创建菜单栏 同时添加File菜单项
    QMenu *file = menuBar()->addMenu(tr("文件"));
    file->addAction(openAction);//将动作绑定到菜单上

    //创建工具栏
    QToolBar *toolBar = addToolBar(tr("文件工具"));
    toolBar->addAction(openAction);

    //创建状态栏
    statusBar();
}

//MainWindow的析构函数
MainWindow::~MainWindow()
{
}

//触发的函数
void MainWindow::open()
{
    QMessageBox::information(this, tr("Information"), tr("文件打开啦"));
}
```

---
## 资源文件

上一节中，我们给动作加图标Icon用到的图像文件，需要从资源文件中加载  
Qt的资源文件是将运行时所需要的资源，以二进制的形式放在可执行文件内部  

### 创建资源

在Qtcreator创建时，是在左边“文件和类”中选择创建Qt资源文件  
创建完成后可在项目中看到创建的资源文件夹，选中后在下方编辑器选择添加-添加前缀  
添加前缀类比为子文件夹，比如我们可以添加一个/images前缀来存放图片信息  
向这个前缀文件夹中添加文件，例如open.png  

### 使用资源

添加的资源文件，可以编辑它的别名例如将open.png文件的别名设置为openIcon  
在使用open.png时可以用这个别名，避免修改文件名引起大量的代码修改  
使用：/images/openIcon来引用资源  

---
## 对象模型

Qt扩展了C++的对象模型，在用C++编译Qt程序之前，先用moc（元对象编译器）工具对Qt代码进行一次预处理，然后再使用C++编译器来编译代码  
例如信号函数可以不编写实现代码（不符合c++）就是moc进行了处理之后的补充完整了语法的原因  

### moc扩展的特性  

* 信号槽  
* 事件机制  
* 上下文字符串翻译（tr函数）  
* 复杂定时器   
* 层次化可查询对象树   
* 智能指针  
* 跨越库边界的动态转换机制  


### 对象树

- QObject是以对象树的形式组织起来的，当创建一个QObject对象时，其构造函数接受一个QObject指针作为参数，这个参数是parent，即父对象指针  
- 例子可以参照MainWindow例子中创建窗口时传入了一个parent参数  
- 这相当于，在创建QObject对象时，可以提供一个父对象，我们创建的这个QObject对象会添加到父对象的`childern()`列表  
- 当父对象析构的时候，该列表也会被析构  
- 这个父对象不是继承意义上的父类  

例如：某按钮有一个子对象是快捷键对象，当我们删除按钮时，这个对象也会被一并删除  


### QWidget  

QWidget是能够在屏幕上显示的一切组件的父类，它继承自QObject，自然也有这种对象树关系  
孩子自动成为父组件的一个子组件，它会显示在父组件坐标系统中，被父组件的边界剪裁  

我们也可以自己删除子对象  

### 内存问题

对象树解决了一定的内存问题  
当一个QObject对象在堆上创建的时候，Qt会同时为其创建对象树  
对象树中的对象没有顺序，同样销毁对象也没有顺序  

删除QObject对象时，如果这个对象有parent，则自动将其从parent的`childer()`列表中删除；如果有孩子，则删除所有孩子  

```cpp
{
    QPushButton quit("Quit");
    QWidget window;

    quit.setParent(&window);
}
```

以上代码会在析构顺序上出现问题  
析构时，先删除window对象（最后一个被创建的被第一个删除）， 此时由于quit是其子对象，quit也会被析构。
析构完window对象后，接着析构quit，但quit已经在上述过程中被析构过了，重复析构就会崩溃  
因此要求我们在构造的时候就要指定parent对象  

---
## 布局管理器

两种定位机制:绝对定位，相对定位  
绝对定位没有给出组件响应窗口变化的方法，当窗口大小改变时，组件的绝对位置并没有改变  
针对这种情况，Qt使用布局解决  

### 布局

把组件放进布局管理器中调整  

```cpp
#include <QApplication>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QSpinBox>
#include <QSlider>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QWidget window;
    window.setWindowTitle("WINDOW");

    //只能输入数字的输入框，并且带有上下箭头，他的父窗口是window
    QSpinBox *spinBox = new QSpinBox(&window);

    //滑动条（水平方向）
    QSlider *slider = new QSlider(Qt::Horizontal, &window);
    
    //调整范围
    spinBox->setRange(0, 130);
    slider->setRange(0, 130);

    //设置信号槽，滑动条数值改变时，将spinBox的数值随之改变
    QObject::connect(slider, &QSlider::valueChanged, spinBox, &QSpinBox::setValue);

    //SpinBox有两个valueChanged函数，编译器不知道该使用那一个
    //设定一个函数指针，指向valueChanged函数
    void(QSpinBox::*spinBoxSignal)(int) = &QSpinBox::valueChanged;

    //信号槽:spinBox数值改变时，也同步修改滑动条的值
    QObject::connect(spinBox, spinBoxSignal, slider, &QSlider::setValue);
    
    //设置初始值
    spinBox->setValue(35);

    //创建水平布局
    QHBoxLayout *layout = new QHBoxLayout();
    
    //水平方向依次添加两个控件
    layout->addWidget(spinBox);
    layout->addWidget(slider);
    
    //窗口应用布局
    window.setLayout(layout);

    window.show();

    return app.exec();
}
```

### 布局的父对象问题

测试程序1： 

```
QWidget * wid = new QWidget(this);
qDebug() << "wid地址:"<<wid;

QLabel *label = new QLabel("label");
QVBoxLayout * layout = new QVBoxLayout;
layout->addWidget(label);

qDebug() << "label 父对象地址1: "<<label->parent();
qDebug() << "layout 父对象地址1: "<<layout->parent();

wid->setLayout(layout);

qDebug() << "label 父对象地址2: "<<label->parent();
qDebug() << "layout 父对象地址2: "<<layout->parent();
```

输出结果：  

```
wid地址: QWidget(0x1ecb9458)
label 父对象地址:  QObject(0x0)
layout 父对象地址:  QObject(0x0)
label 父对象地址:  QWidget(0x1ecb9458)
layout 父对象地址:  QWidget(0x1ecb9458)
```

程序中对于label和layout都没有制定parent，因此它们被new出来后，内存管理就存在疑问  
但是通过打印结果，可以发现没有parent的布局在`setlayout`后都有了parent

那么对于在new的时候就指定了parent的情况呢？

测试程序2： 

```
QWidget * wid = new QWidget(this);
qDebug() << "wid地址:"<<wid;

QLabel *label = new QLabel("label", this);//此时的label和wid都是this的child
QVBoxLayout * layout = new QVBoxLayout;
layout->addWidget(label);

qDebug() << "label 父对象地址1: "<<label->parent();
qDebug() << "layout 父对象地址1: "<<layout->parent();

wid->setLayout(layout);

qDebug() << "label 父对象地址2: "<<label->parent();
qDebug() << "layout 父对象地址2: "<<layout->parent();
```

输出结果：

```
wid地址: QWidget(0x206d9938)
label 父对象地址1:  MainWindow(0x7afe00)
layout 父对象地址1:  QObject(0x0)
label 父对象地址2:  QWidget(0x206d9938)
layout 父对象地址2:  QWidget(0x206d9938)
```

原来同级的wid和label，在label被setlayout到wid中时，label的parent变成了wid  
因此，在设置layout时，可以不必指定parent  

### 布局管理器

* QHBoxLayout 按照水平方向左到右  
* QVBoxLayout 按照竖直方向上到下  
* QGridLayout 网格中进行布局  
* QFormLayout 表格布局 类似HTML的form  
* QStackedLayout 层叠布局，在Z轴上堆叠  

---
## 对话框

很多不能或不合适放入主窗口的功能组件都必须放在对话框中设置  
对话框是一个顶层窗口，出现在程序最上层，用于实现短期任务或用户交互  

### QDialog类

实现对话框，像主窗口一样，通常设计一个类继承QDialog  

顶层窗口：任务栏有一个独占的位置   
非顶层窗口： 共享父组件的位置  

对于QDiaglog的parent指针：parent为NULL，表示该对话框最为顶层窗口，否则作为父组件的子对话框，默认在parent的中心  

```cpp
// 顶层对话框
void MainWindow::open()
{
    QDialog dialog;
    dialog.setWindowTitle(tr("dialog~~~"));
    dialog.exec();//循环监听
}

// 非顶层对话框
void MainWindow::open()
{
    QDialog dialog(this);
    dialog.setWindowTitle(tr("dialog~~~"));
    dialog.exec();
}
```

### 模态 非模态

1. 模态对话框：阻塞程序中其他窗口的输入，例如打开文件，打开文件对话框出现时，不能对其他窗口操作  
1. 非模态对话框：可以继续对窗口编辑  


- 应用级模态（默认，dialog.exec()）：不能操作程序其他窗口  
- 窗口级模态（dialog.show()）：可以操作应用的其他窗口，仅阻塞与对话框关联的窗口，适用于多窗口模式  
- 非模态：dialog.open()


### 非模态的问题

在栈上建立的`dialog.show()`不会阻塞当前线程  
对话框刚显示，就执行完毕立即返回，代码继续执行，这个栈上的对话框内存会被释放  

因此要把改为在堆上建立（new）  

```cpp
QDialog *dialog = new QDialog;
dialog->setWindowTitle(tr("~~"));
dialog->show();
```

但这样会导致内存泄露（new出的内存未通过delete释放）  
解决方法是将MainWindow的指针赋值给dialog  
这样按照对象树，dialog是MainWindow的children,当MainWindow销毁时，也会销毁dialog  
但是，这样一来，在MainWindow没有销毁之前，还是会一直占用内存  

还可以设置dialog的WindowAttribute，让dialog在关闭时销毁(close时调用delete)  

```cpp
void MainWindow::open()
{
    QDialog *dialog = new QDialog;
    dialog->setAttribute(Qt::WA_DeleteOnClose); // 关闭对话框时自动销毁
    dialog->setWindowTitle(tr("~~"));
    dialog->show();
}
```

---
## 对话框数据传递

对话框用于完成比较简单或短期的任务  
对话框中输入的数据需要和主窗口进行交互  

### 模态对话框

模态使用了exec()函数显示（开启新的事件无限循环 等待结束）  
该循环保证能够监听程序  
监听事件也相当于轮询  
因此，在这个无限循环之后的程序不会被执行即代码被阻塞  
这就是为什么模态对话框出现时，不能和主窗口交互的原因  

所以在循环结束后，才可以获取到对话框中输入的数据  
```cpp
void MainWindow::open()
{
    QDialog dialog(this);//出了该函数就自动销毁
    dialog.setWindowTitle(tr("Hello dialog"));
    dialog.exec(); // 此时一直循环执行对话框
    qDebug() << dialog.result();//对话框关闭后获取值  
}
```

如果在这里将dialog的属性设置为WA_DeleteOnClose，那么对话框被关闭时就会销毁，没办法获取数据  
这时候可以使用parent指针的方式构建对话框避免设置WA_DeleteOnClose属性  

实际上QDialog::exec()是有返回值的，其返回值是QDialog::Accepted或者QDialog::Rejected  
可以通过下面的例子判断点击了确定还是取消  

```cpp
QDialog dialog(this);
if (dialog.exec() == QDialog::Accepted)
{
    //do something
}else{
    //do something else
}
```

### 非模态对话框

非模态用的是show()，`QDialog::show()`函数会立即返回，这样也不能得到用户输入的数据  
因为show()不想exec执行死循环阻塞主线程，会立即返回，还没有输入就要执行后面的代码  

所以在需要传递参数信息时，不建议使用非模态对话框  

非模态可以使用信号槽机制来传递数据，在对话框关闭时触发一个信号，发送数据  
重写`QDialog::closeEvent()`函数，发出信号，在需要接受数据的窗口连接到这个信号  

```cpp
void MainWindow::showUserAgeDialog()
{
    UserAgeDialog *dialog = new UserAgeDialog(this);
    connect(dialog, &UserAgeDialog::userAgeChanged, this, &MainWindow::setUserAgeChanged);
    dialog->show();
}

void UserAgeDialog::accept()
{
    emit userAgeChanged(newAge);
    QDialog::accept();
}


void MainWindow::setUserAgeChanged(int age)
{
    userAge = age;
}
```

---
## 标准对话框-QMessageBox

Qt内置了一系列的对话框  
这些对话框都是很通用的  

```
    QColorDialog：选择颜色；
    QFileDialog：选择文件或者目录；
    QFontDialog：选择字体；
    QInputDialog：允许用户输入一个值，并将其值返回；
    QMessageBox：模态对话框，用于显示信息、询问问题等；
    QPageSetupDialog：为打印机提供纸张相关的选项；
    QPrintDialog：打印机配置；
    QPrintPreviewDialog：打印预览；
    QProgressDialog：显示操作过程。
```

### 内置的static函数  

```cpp
//关于对话框 包含标题 内容 父窗口，对话框只有一个OK按钮
void about(QWidget * parten, const QString & title, const QString & text)

类似的还有：
void aboutQt:显示关于Qt对话框
StandardButton critical：显示严重错误对话框，只有OK按钮
StandardButton information：与critical一致，单提供一个信息图形
StandardButton question：提供一个问号图标，并显示按钮“是”和“否”
StandardButton warning:提供黄色叹号图标
```

### QMessageBox

```cpp
if (QMessageBox::Yes == QMessageBox::question(this,
                                              tr("Question"),
                                              tr("Are you OK?"),
                                              QMessageBox::Yes | QMessageBox::No,
                                              QMessageBox::Yes)) 
{
    QMessageBox::information(this, tr("Hmmm..."), tr("I'm glad to hear that!"));
} 
else 
{
    QMessageBox::information(this, tr("Hmmm..."), tr("I'm sorry!"));
}
```

### 更灵活使用

内置的对话框使用方便但是不灵活  
可以如下进行自定义  

```cpp
QMessageBox msgBox;

msgBox.setText(tr("The document has been modified."));
msgBox.setInformativeText(tr("Do you want to save your changes?"));
msgBox.setDetailedText(tr("Differences here..."));
msgBox.setStandardButtons(QMessageBox::Save
                          | QMessageBox::Discard
                          | QMessageBox::Cancel);
msgBox.setDefaultButton(QMessageBox::Save);

int ret = msgBox.exec();
switch (ret) 
{
case QMessageBox::Save:
    qDebug() << "Save document!";
    break;
case QMessageBox::Discard:
    qDebug() << "Discard changes!";
    break;
case QMessageBox::Cancel:
    qDebug() << "Close document!";
    break;
}
```
这里注意setDetailedText,它的信息不显示在对话框中，而是在对话框上加了一个按钮，只有点击按钮才会显示出该信息  


---
## Qt5信号槽新语法  

在信号槽实现观察者模式时  

```cpp
QObject::connect(&newspaper, &Newspaper::newPaper &reader, &Reader::receiveNewspaper);
```

这里使用了取地址符`&`操作到函数的地址，可以在编译期进行检查  

### C++函数指针

指针指向函数的地址  

```cpp
void add(int a, double b)
{
    cout << a + b << endl;
}

int main()
{
    //本类的函数
    void (* pAdd)(int a, double b) = add;

    //其他类的函数,必须加上类名和取地址符
    void (* pAdd)(int a, double b) = &otherClass::add;

    //调用
    int a = 1;
    int b = 4;
    (*pAdd)(a, b);
    pAdd(a, b);

    return 0;
}
```


### 重载信号  

如果Newspaper类中的newPaper信号函数有重载  
例如又添加了如下：  

```cpp
void newPaper(const QString &name, const QDate &date);
```
那么此时connect函数就会报错，因为connect中不需要写函数参数，因此不知道该使用重载的哪个函数  

可以使用函数指针来指明使用的是哪一个信号：  

```cpp
//指针:newPaperNameDate指向函数Newspaper::newPaper
void (Newspaper:: *newPaperNameDate)(const QString &, const QDate &) = &Newspaper::newPaper;

//指针已经指向了特殊函数的地址
QObject::connect(&newspaper, newPaperNameDate,
                 &reader,    &Reader::receiveNewspaper);
```

也可以将以上两部分直接合并在一起  

```cpp
QObject::connect(&newspaper,
                 static_cast<void (Newspaper:: *)(const QString &, const QDate &)>(&Newspaper::newPaper),
                 &reader,
                 &Reader::receiveNewspaper);
```

### 带默认参数的槽函数

一般情况下，槽函数参数可以少于信号函数的参数  
但有例外情况，即槽函数参数中有默认的参数  

```cpp
// Newspaper
signals:
    void newPaper(const QString &name);

// Reader
    void receiveNewspaper(const QString &name, const QDate &date = QDate::currentDate());
```

这样的话，又出现了新的问题，C++使用函数指针取其地址时，默认参数不可见  
有两个解决办法：  

1. 使用Qt4语法,connect可以加函数参数  

```cpp
QObject::connect(&newspaper, SIGNAL(newPaper(QString, QDate)),
                 &reader,    SLOT(receiveNewspaper(QString, QDate)));
```

2. Lambda表达式  

```cpp
QObject::connect(&newspaper,
                 static_cast<void (Newspaper:: *)(const QString &)>(&Newspaper::newPaper),
                 [=](const QString &name) { /* Your code here. */ });
```


---
## 文件对话框  

QFileDialog也是一个标准对话框  
例子：完成一个文本编辑器  

### 制作带有文本编辑功能的窗口

```cpp
//创建一个打开动作
openAction = new QAction(QIcon(":/images/file-open"), tr("&Open..."), this);
openAction->setShortcuts(QKeySequence::Open);
openAction->setStatusTip(tr("Open an existing file"));

//创建一个关闭动作
saveAction = new QAction(QIcon(":/images/file-save"), tr("&Save..."), this);
saveAction->setShortcuts(QKeySequence::Save);
saveAction->setStatusTip(tr("Save a new file"));

//创建菜单栏，添加 打开与关闭
QMenu *file = menuBar()->addMenu(tr("&File"));
file->addAction(openAction);
file->addAction(saveAction);

//创建状态栏
QToolBar *toolBar = addToolBar(tr("&File"));
toolBar->addAction(openAction);
toolBar->addAction(saveAction);

//显示富文本文件
textEdit = new QTextEdit(this);

//将组件放置在窗口中央显示区
setCentralWidget(textEdit);
```

### 为动作链接响应

```cpp
///当openAction触发时，链接到主窗口的openFile函数，下同
connect(openAction, &QAction::triggered, this, &MainWindow::openFile);

connect(saveAction, &QAction::triggered, this, &MainWindow::saveFile);
```

### 添加被链接的函数openFile saveFile

```cpp
void MainWindow::openFile()
{
    //获取用户选定的文件路径
    QString path = QFileDialog::getOpenFileName(this, tr("Open File"), ".", tr("Text Files(*.txt)"));
    if(!path.isEmpty()) 
    {
        //根据路径创建QFile对象
        QFile file(path);
        //打开文件，只读方式|文本方式
        if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) 
        {
            QMessageBox::warning(this, tr("Read File"), tr("Cannot open file:\n%1").arg(path));
            return;
        }

        //读取文件所有内容赋值给QTextEdit显示出来
        QTextStream in(&file);
        textEdit->setText(in.readAll());
        file.close();
    } 
    else 
    {
        QMessageBox::warning(this, tr("Path"), tr("You did not select any file."));
    }
}

void MainWindow::saveFile()
{
    QString path = QFileDialog::getSaveFileName(this, tr("Open File"), ".", tr("Text Files(*.txt)"));
    if(!path.isEmpty()) 
    {
        QFile file(path);
        if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
        {
            QMessageBox::warning(this, tr("Write File"), tr("Cannot open file:\n%1").arg(path));
            return;
        }
        QTextStream out(&file);
        out << textEdit->toPlainText();
        file.close();
    } 
    else 
    {
        QMessageBox::warning(this, tr("Path"), tr("You did not select any file."));
    }
}
```

```cpp
//打开文件对话框中 获取文件名函数有多个可选参数
//返回选择的文件路径
QString getOpenFileName(QWidget * parent = 0,//父窗口
                        const QString & caption = QString(),//窗口标题
                        const QString & dir = QString(),//打开的默认目录，“.” 代表程序运行目录，“/” 代表当前盘符的根目录
                        const QString & filter = QString(),//过滤器，多个过滤器使用；号连接“JPEG Files(*.jpg);;PNG Files(*.png)”
                        QString * selectedFilter = 0,//默认选择的过滤器
                        Options options = 0)//对话框参数设定
```

---
## 事件

事件是由系统或Qt自身发出的  
当用户点击鼠标，敲击键盘时都会发出一个事件  
也有系统自己发出的事件：定时器  

C语言等是线性执行的，这种批处理风格不适合处理复杂的事务  
事件驱动是由事件触发执行代码，如果没有事件，就一直阻塞不执行任何事件  
事件驱动类似于Qt的信号槽机制，但这两个不能等同  

信号是由具体的对象发出的，交给connect链接的槽函数  
事件可以使用事件过滤器进行过滤，有些事件不予处理  
因此 当使用组件时，关注的是信号槽，如果自定义组件时，关心的是事件  

QCoreApplication中的exec（）函数就是监听Qt的事件循环，当事件发生时，用来监听  
当事件发生时，先创建一个事件对象，它继承与QEvent，在创建完毕后，将这个对象传递给QObject的envent函数  
envent函数将事件按类型分给特定的事件处理函数event hadler  

### 鼠标事件示例

```cpp
//继承QLabel
class EventLabel : public QLabel
{
protected:
    //重写三个事件处理函数
    void mouseMoveEvent(QMouseEvent *event);
    void mousePressEvent(QMouseEvent *event);
    void mouseReleaseEvent(QMouseEvent *event);
};

void EventLabel::mouseMoveEvent(QMouseEvent *event)
{
    //事件发生时显示内容
    //Label支持HTML
    //QString().arg()格式化字符串
    this->setText(QString("<center><h1>Move: (%1, %2)</h1></center>")
                  .arg(QString::number(event->x()), QString::number(event->y())));
}

void EventLabel::mousePressEvent(QMouseEvent *event)
{
    this->setText(QString("<center><h1>Press: (%1, %2)</h1></center>")
                  .arg(QString::number(event->x()), QString::number(event->y())));
}

void EventLabel::mouseReleaseEvent(QMouseEvent *event)
{
    //C风格输出
    QString msg;
    msg.sprintf("<center><h1>Release: (%d, %d)</h1></center>",
                event->x(), event->y());
    this->setText(msg);
}

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    //注意这里要释放
    EventLabel *label = new EventLabel;
    label->setWindowTitle("MouseEvent Demo");
    label->resize(300, 200);
    
    //开启鼠标追踪，否则是在单击之后才进行追踪
    label->setMouseTracking(true);
    label->show();

    return a.exec();
}

```

---
## 事件的接受与忽略

### 事件在子类中的重写

子类重写了父类的回调函数后，要注意调用父类的同名函数来确保原有实现仍能进行  
比如QPushButton中有一个mousePressEvent事件，执行操作A，子类CustomButton继承父类后重写了这个事件  

```cpp
void CustomButton::mousePressEvent(QMouseEvent *event)
{
    if(event->button() == Qt::LeftButton)
    {
        //子类操作
    }
    else
    {
        QPushButton::mousePressEvent(event);//执行父类函数
    }
}
```

在当符合某个条件时，执行子类特有的操作，否则执行父类的操作  
类似于构造函数，子类的构造函数又是会调用父类的构造函数  

### 事件的accept和ignore

子类是否处理该事件？  
1. 如果子类处理(accept)则不再继续传播，到此为止  
1. 如果子类不处理(ignore)就继续向**父组件**传递  

accept某个事件后，该事件传播到此为止,不会再传播  
ignore事件，则表示不想处理该事件,事件会继续向**父组件**传播寻找接受者(注意不是传播给父类)  
可以使用isAccepted()来查询事件是否被接收  
事件的传播是在组件层次上的,而不是靠类继承机制!  

### 常用的处理方式  

常常不显示地使用accept和ignore来处理事件,而是通过调用父类的事件函数来达到忽略事件的目的  
因为事件是会**传递到父组件上的,而不是给父类**  
我们无法确定,父类对这个事件是否有额外的操作,所以为了不发生意外,在子类的事件函数重写时,都调用父类的事件处理函数  
Qt中所有组件的父类QWidget默认调用ignore，因此再向父类传递时，如果没有特殊操作那么该事件都会被默认ignore  

而事件本身默认是accept，所以对于组件a和事件e：  
1. 如果a不需要对e处理，我们就调用a的父类对e处理  
1. 如果a的父类以及父类的父类都没有处理，e就会一直传递给最高的父类QObject  
1. QObject默认会处理这个事件为ignore，然后e就会被传播到组件a的父组件A  
1. 如果父组件A也不处理，就一直向上找  
1. 如果到了最后，事件e没有被任何类，任何组件处理，就会一直传播到尽头，但事件默认是accept，因此传播终止  


## event()

Qt将事件对象创建完毕之后,传递给`event()`函数  
`event()`函数**不直接处理事件**,它按照不同的类型(type)将该事件**分发**给不同的事件处理器  
可以将`event()`函数看作是事件的分发器,修改它就可以操纵事件在被分发前的过程  

### 监听tab键的按下

假设CustomWidget继承自Qwidget  
重写event函数

```cpp
bool CustomWidget::event(QEvent *e)
{
    //如果发生的事件类型(type)是KeyPress(枚举型),就继续判断是否为要处理的tab
    if (e->type() == QEvent::KeyPress) 
    {
        //QEvent强制转换为QKeyEvent
        QKeyEvent *keyEvent = static_cast<QKeyEvent *>(e);

        //如果按下的是tab键,进行特殊处理
        if (keyEvent->key() == Qt::Key_Tab) 
        {
            qDebug() << "You press tab.";
            //返回ture代表该事件已被成功识别并处理(事件默认accept)
            return true;
        }
    }

    //发生的不是关注的事件,就调用父类函数继续处理
    return QWidget::event(e);
}
```

在`envent()`函数里,accept和ignore没有作用,因为其只是分发事件,而并不是处理事件  
分发事件是否成功的标志是bool值  
如果返回的是true并且该事件被accept,则说明这个事件被分发成功且已被处理,Qt就不会继续向上层组件传播该事件  

```cpp
//修改上述代码的最后一行
return QWidget::event(e);
//改为
return false;
```

则除了tab键会在转发时被直接处理外,其它的任何事件都不会被转发出去  
所以一定要注意重写envent()时要同时调用父类的event()

### 修改与屏蔽事件

QObejct的event()函数

```cpp
bool QObject::event(QEvent *e)
{
    //在分发事件前,先查找自己关心的事件,执行该事件对应的事件处理函数
    switch (e->type()) 
    {
    case QEvent::Timer:
        timerEvent((QTimerEvent*)e);
        break;
 
    case QEvent::ChildAdded:
    case QEvent::ChildPolished:
    case QEvent::ChildRemoved:
        childEvent((QChildEvent*)e);
        break;
    default:
        if (e->type() >= QEvent::User) 
        {
            customEvent(e);
            break;
        }
        return false;
    }

    return true;
}
```

如果想修改某个事件,如`mouseMoveEvent`,一般不需要重写`event()`,因为event中会在switch中调用`mouseMoveEvent()`,所以只需重写`mouseMoveEvent()`即可  

如果,父类event()关注的事件(switch分支)过多,而子类不再想关注这些,只想对一部分事件进行关注,如tab.那么就可以重写event()函数,修改switch分支  

简短来说:event()是一个集中处理不同类型事件的地方,将事件具体"委托"给某一个事件处理器  

---
## 事件过滤器

一个模态对话框需要屏蔽用户按键不让其它组件接收到  
那么,如上节所言,可以重写event函数(),删除要屏蔽的switch分支  
但,如果switch中的分支很多,则这样做就太麻烦,且要小心翼翼防止改错  

Qt提供了事件过滤器eventFilter()这一机制来完成这个目的  

函数签名:

```cpp
virtual bool QObject::eventFilter ( QObject * watched, QEvent * event );
```

事件过滤器会检查接收到的事件,如果是感兴趣的则自己处理,否则继续转发  
在目标对象(即watched对象)收到事件之前,就过滤事件,停止事件的转发并返回true.否则返回false 

### 示例

```cpp
//继承QMainWindow类的子类MainWindow
class MainWindow : public QMainWindow
 {
 public:
     MainWindow();
 protected:
     bool eventFilter(QObject *obj, QEvent *event);
 private:
     QTextEdit *textEdit;
 };

 MainWindow::MainWindow()
 {
     textEdit = new QTextEdit;
     setCentralWidget(textEdit);
    
     //给textEdit安装过滤器
     //textEdit对象的事件都会先发送到MainWindow上的eventFilter中进行过滤处理
     //可以给多个对象安装过滤器
     textEdit->installEventFilter(this);
 }

 bool MainWindow::eventFilter(QObject *obj, QEvent *event)
 {
     //如果对象是textEdit,进一步判断
     if (obj == textEdit) 
     {
         //如果是键盘输入事件,则过滤,返回true
         if (event->type() == QEvent::KeyPress) 
         {
             QKeyEvent *keyEvent = static_cast<QKeyEvent *>(event);
             qDebug() << "Ate key press" << keyEvent->key();
             //返回true,表明过滤掉这个event
             return true;
         } 
         else 
         {
             //不是要过滤的事件,返回false.对这个event不操作
             return false;
         }
     } 
     else 
     {
         //因为不知道父类是否还要进行其它过滤,因此要调用父类的过滤器
         return QMainWindow::eventFilter(obj, event);
     }
 }
```

给对象安装过滤器使用`installEventFilter()`  
同一个对象可以安装多个过滤器,**最后安装的最先执行**  
卸载过滤器使用`removeEventFilter()`  

installEventFilter()是QObject的函数,意味着任何QObject的子类都可以被安装过滤器,即使是QApplication  
全局的过滤器会最先被调用,但复杂的过滤器会严重影响到效率  

---
## 事件总结

Qt中的事件可以类比windows中的消息机制  
事件有鼠标,键盘,位置移动事件  
每个事件一般都会有对应的事件处理函数,如mouseMoveEvent等  
那么就要有一个switch分支,将传来的事件信息和事件处理函数进行链接起来(分发)  

### 修改事件的几个层级

1. 重写事件处理函数mouseMoveEvent()来修改事件  
1. 重写event()函数,让事件分发给另一个事件处理函数,或者直接在event中进行处理,不再向下分发  
1. 添加事件过滤器,在事件发送个event函数之前,先对特定事件进行过滤,或处理.给QApplication安装的过滤器会导致所有对象上的事件都先经过该过滤器  

### 示例

```cpp
class Label : public QWidget
{
public:
    Label()
    {
        //在构造函数中安装过滤器
        installEventFilter(this);
    }

    //重写过滤器,对关注的事件进行过滤
    bool eventFilter(QObject *watched, QEvent *event)
    {
        //如果是过滤的对象是label
        if (watched == this) 
        {
            //按压鼠标按键
            if (event->type() == QEvent::MouseButtonPress) 
            {
                qDebug() << "eventFilter";
            }
        }

        //所有事件都不过滤，只是在MouseButtonPress事件被转发前加了一行打印
        return false;
    }

protected:
    void mousePressEvent(QMouseEvent *)
    {
        qDebug() << "mousePressEvent";
    }

    //事件分发
    bool event(QEvent *e)
    {
        if (e->type() == QEvent::MouseButtonPress)
        {
            qDebug() << "event";
        }

        return QWidget::event(e);
    }
};

class EventFilter : public QObject
{
public:
    EventFilter(QObject *watched, QObject *parent = 0) :
        QObject(parent),
        m_watched(watched)
    {
    }

    bool eventFilter(QObject *watched, QEvent *event)
    {
        if (watched == m_watched) 
        {
            if (event->type() == QEvent::MouseButtonPress) 
            {
                qDebug() << "QApplication::eventFilter";
            }
        }
        return false;
    }

private:
    QObject *m_watched;
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    Label label;
    app.installEventFilter(new EventFilter(&label, &label));
    label.show();
    return app.exec();
}
```

鼠标点击之后的输出结果为:

```cpp
//全局过滤器输出,并未终止该事件,事件继续传播下去
QApplication::eventFilter 

//事件传播到label对象,在给label的event之前,被过滤器捕捉到,但同样没有终止它
eventFilter 

//进入event分发事件
event 

//进入事件处理函数
mousePressEvent
```
---
## 自定义事件

Qt内嵌的事件有时是不能满足我们的需求的,比如在其它终端设备上可能没有鼠标键盘事件而是触摸事件等等  
为什么是事件而不是信号槽?  
主要原因是事件的分发可以同步也可以异步还可以过滤  
而槽的回调总是同步的  

### 创建自定义事件

Qt的事件类是QEvent,自定义事件需要继承这个类  
继承该类需要提供一个QEvent::Type类型的参数,作为类型(事件都是有类型的)  
QEvent::type()是QEvent定义的一个枚举,传入的type可以是一个int值,但要保证不能重复  

type是有范围的,0-999为系统保留.我们定义自己的枚举值是要介于QEvent::User与QEvent::MaxUser之间(1000-65535)  
在这个区间的值不会与系统内定的type值冲突,但可能会与其它自定的枚举值冲突  
为了保证不冲突,可以使用`static int QEvent::registerEventType(int hint = -1)`来分配type值,默认hint是-1,返回一个新type值,如果自己指定了以hint作为type值且不冲突,则该函数返回hint,否则返回一个新的合法值  

### 发送自定义事件
Qt有两种事件发送方式:  
1. sendEvent  
1. postEvent  

#### sendEvent()

```cpp
static bool QCoreApplication::sendEvent(QObject *receiver, QEvent *event);
```

直接将envent事件发送给接受者,返回事件处理函数的返回值  
事件发送时不会被销毁,通常在栈上创建event对象  

```cpp
QMouseEvent event(QEvent::MouseButtonPress, pos, 0, 0, 0);
QApplication::sendEvent(mainWindow, &event);
```

#### postEvent()

```cpp
static void QCoreApplication::postEvent(QObject *receiver, QEvent *event);
```

该函数将事件追加到事件队列中,立即返回,不等待处理结果  
在队列中的事件被post后才会被delete掉,因此必须在堆上创建event对象  
事件是按照post的顺序进行处理,改变顺序可以指定一个优先级,默认为Qt::NormalEventPriority  

### 处理自定义事件

接收到自定义事件后要对其进行专门的处理

```cpp
bool CustomWidget::event(QEvent *event) 
{
    //通过自定义事件的type来判断
    if (event->type() == MyCustomEventType) 
    {
        CustomEvent *myEvent = static_cast<CustomEvent *>(event);
        // processing...
        return true;
    }
    return QWidget::event(event);
}
```

---
## 绘制系统

Qt的绘制系统主要包含三个类QPainter QPainterDevice QPaintEngine  

- QPainter用于执行绘图操作  
- QPainterDevice是绘制空间,如纸,屏幕等  
- QPaintEngine是一个接口,将QPainter和QPainterDevice匹配起来,或者说将QPainter的指令翻译为QPainterDevice能够识别的指令  

```cpp
//接受QPainterDevice参数,创建画笔 理解为在当前组件上(this)画图
QPainter painter(this);
painter.drawLine(80, 100, 650, 500);

//更换画笔颜色
painter.setPen(Qt::red);
painter.drawRect(10, 10, 100, 400);

//更换颜色 宽带
painter.setPen(QPen(Qt::green, 5));

//设置画刷
painter.setBrush(Qt::blue);
painter.drawEllipse(50, 150, 400, 200);
```  

## 画刷和画笔  

- 画刷QBrush用于填充  
- 画笔QPen用于画轮廓线  

### QBrush

定义QPainter的填充模式,具有样式 颜色 纹理 渐变等属性  
- 样式(style):使用Qt::BrushStyle枚举,共有19种样式，默认为Qt::NoBrush  
- 颜色(color):可以用预定义的颜色常量Qt::GlobalColor,也可以为QColor对象  
- 渐变(gradient):能够使用渐变取决于当前的样式是否支持  
  - 只有在样式为Qt::LinearGradientPattern、Qt::RadialGradientPattern或Qt::ConicalGradientPattern之一时才有效  
  - 渐变可以由QGradient对象表示  
  - Qt 提供了三种渐变对象：QLinearGradient、QConicalGradient和QRadialGradient，均为QGradient的子类
- 纹理(texture):只有样式为Qt::TexturePattern时才可用纹理,texture()定义纹理.如果调用setTexture()时,会自动修改样式

```cpp
//创建一个QRadialGradient渐变对象
QRadialGradient gradient(50, 50, 50, 50, 50);

//设置渐变对象的参数
gradient.setColorAt(0, QColor::fromRgbF(0, 1, 0, 1));
gradient.setColorAt(1, QColor::fromRgbF(0, 0, 0, 0));

//将这个渐变对象添加到画刷中
QBrush brush(gradient);
```


### QPen

定义了如何画线或者轮廓线  

- 属性: 
  - 样式style：直线，点线，点划线(Qt::SolidLine Qt::DashLine Qt::DotLine)等  
  - 宽度width：线条的宽度  
  - 画刷brush:填充画笔绘制的线条  
  - 笔帽样式capStyle:线的末端样式(Qt::SquareCap Qt::FlatCao Qt::RoundCap)  
  - 连接样式joinStyle：两条线衔接处的图形样式(Qt::BevelJoin Qt::MiterJoin Qt::RoundJoin)  
- 默认属性为 黑色 0像素 方形笔帽 斜面型连接  

```cpp
QPainter painter(this);

//设置画笔参数
QPen pen;
pen.setStyle(Qt::DashDotLine);
pen.setWidth(3);
pen.setBrush(Qt::green);
pen.setCapStyle(Qt::RoundCap);
pen.setJoinStyle(Qt::RoundJoin);

//也可以在创建画笔时设定参数
//QPen pen(Qt::green, 3, Qt::DashDotLine, Qt::RoundCap, Qt::RoundJoin);

//给painter绑定画笔
painter.setPen(pen);
```

## 反走样

即消除在光栅图形显示器上的锯齿  

```cpp
QPainter painter(this);
painter.setPen(QPen(Qt::black, 5, Qt::DashDotLine, Qt::RoundCap));
painter.setBrush(Qt::yellow);
painter.drawEllipse(50, 150, 200, 150);

//设置反走样开启
painter.setRenderHint(QPainter::Antialiasing, true);
painter.setPen(QPen(Qt::black, 5, Qt::DashDotLine, Qt::RoundCap));
painter.setBrush(Qt::yellow);
painter.drawEllipse(300, 150, 200, 150);
```

反走样由于效率问题,一般不默认开启

## 渐变

- 从一种颜色到另一种颜色逐渐过渡  
- 在QBrush中设置,Qt提供了三种:线性(QLinearGradient) 辐射(QRadialGradient) 角度(QConicalGradient)  

### 线性渐变举例

```cpp
QPainter painter(this);

//打开反走样
painter.setRenderHint(QPainter::Antialiasing, true);

//新建线性渐变,起始点-终止点
QLinearGradient linearGradient(60, 50, 200, 200);

//在position处[0-1]设置颜色
linearGradient.setColorAt(0.2, Qt::white);
linearGradient.setColorAt(0.6, Qt::green);
linearGradient.setColorAt(1.0, Qt::black);

//设置画刷
painter.setBrush(QBrush(linearGradient));
painter.drawEllipse(50, 50, 200, 150);
```

### 角度渐变举例

渐变圆盘

```cpp
//设置绘制
QPainter painter(this);
painter.setRenderHint(QPainter::Antialiasing);

//设置圆盘半径
const int r = 150;

//设置角度渐变,参数:角度渐变中心点(0,0) 起始角度0
QConicalGradient conicalGradient(0, 0, 0);

//第一个参数为角度
conicalGradient.setColorAt(0.0, Qt::red);
conicalGradient.setColorAt(60.0/360.0, Qt::yellow);
conicalGradient.setColorAt(120.0/360.0, Qt::green);
conicalGradient.setColorAt(180.0/360.0, Qt::cyan);
conicalGradient.setColorAt(240.0/360.0, Qt::blue);
conicalGradient.setColorAt(300.0/360.0, Qt::magenta);
conicalGradient.setColorAt(1.0, Qt::red);

//修改原点为(r,r) 则此时左上点的旧原点坐标坐标为(-r, r)
painter.translate(r, r);

QBrush brush(conicalGradient);
painter.setPen(Qt::NoPen);
painter.setBrush(brush);

//此时原点已变
painter.drawEllipse(QPoint(0, 0), r, r);
```


## 坐标系统

- 逻辑坐标系统由QPainter控制  
- 设备坐标则是在QPaintDevice的图形输出对象上，坐标原点(0,0)默认在左上角，单位是像素(显示器)或点(打印机，1//72英寸)  
- 逻辑坐标与物理坐标的映射由QPainter的变换矩阵(transformation matrix)、视口(viewport)、窗口(window)完成  

### 像素

像素是一个一个的小方格，例如左上角点的像素(0,0)实际上是坐标(0,0) (0,1) (1,1) (1,0)围成的小方格  
换句话说，像素是逻辑坐标右下方的小方格  
因此在使用QRect时，函数`QRect::right()=left() + width() - 1`而`QRect::bottom() = top() + height() - 1`
返回的坐标值与真实坐标值差一  

### QPainter状态

可以临时保存当前的画图状态并在之后恢复
- `save()`函数可以保存当下的状态如坐标系原点，画笔的颜色、粗细，画刷等  
- `restore()`函数可以恢复`save()`保存的结果  
- 这两个函数通过**栈**来实现，必须成对出现  

### 变换示例

- 平移translate  
- 旋转rotate  
- 缩放scale  
- 扭曲shear  

```cpp
QPainter painter(this);

//画矩形
painter.fillRect(10, 10, 50, 100, Qt::red);

painter.save();
painter.translate(100, 0);//坐标系原点右移100
painter.fillRect(10, 10, 50, 100, Qt::yellow);
painter.restore();

painter.save();
painter.translate(300, 0);
painter.rotate(30);//顺时针旋转30度
painter.fillRect(10, 10, 50, 100, Qt::green);
painter.restore();

painter.save();
painter.translate(400, 0);
painter.scale(2,3);//x坐标单位放大2倍，y坐标放大3倍
painter.fillRect(10, 10, 50, 100, Qt::blue);
painter.restore();

painter.save();
painter.translate(600, 0);
painter.shear(0,1);//纵向扭曲1倍
painter.fillRect(10, 10, 50, 100, Qt::cyan);
painter.restore();
```

### 逻辑坐标 设备坐标

- 提供给QPainter绘制的坐标都是逻辑坐标
- 要在设备上绘制就要提供设备的物理坐标
- qt使用viewport-window将逻辑坐标转换为物理坐标，方法是在逻辑坐标和物理坐标间加上一层窗口坐标  

逻辑坐标：窗口 ---> 视口：物理坐标  

#### 窗口（逻辑）

窗口代表逻辑处理的区域  
setWindow()设置窗口大小  

实际大小为200*200的窗口，默认窗口大小为200×200，视口大小也为200×200  
在(0,0)位置画一个100×100的矩形，则占用左上角1/4的大小  
执行setWindow(-50, -50, 100, 100)；  
左上角的物理坐标还是(0, 0)但是逻辑坐标为(-50, -50)  
右下角的物理坐标还是(200, 200)但是逻辑坐标为(50, 50) 

#### 视口（物理）

视口代表实际的绘图区域  
实际大小为200*200的窗口，默认窗口大小为200×200，视口大小也为200×200  
执行setViewPort(0, 0, 100, 100);  
则绘图区域变为原来的1/4  
使用逻辑坐标绘制矩形painter.drawRect(0, 0, 100, 100)；矩形为原图的1/16  

#### 防止变形

由于窗口和视口会不一致，因此为了防止图形在坐标转换时变形需要是两者的**宽高比**一致  

```cpp
int side = qMin(width(), height());
int x = (width() - side/2);
int y = (height() - side/2);
painter.setViewport(x, y, side, side);//逻辑(0,0)映射为(x,y)，逻辑的width()映射为物理的side
```

## 绘制设备

QPainter可以在任何的QPaintDevice的子类上进行绘制  
子类包含：  
- QWidget：所有控件的父类  
- QImage  
- QPixmap  
- QGLFramebufferObject  
- QPicture  
- QPrinter  

QPainter在QWidget中只能在paintEvent()中使用，而其他QPaintDevice没有这个限制

### QPixmap

可以使用QPainter画图，也可以接受一个文件路径显示图像文件(png jepg)  
使用QPainter::drawPixmap()函数可以把文件绘制到QLabel QPushButton或其他设备上  
QPixmap针对屏幕进行了特殊的优化  
提供了“隐式数据传递”不需要显式地传递指针，会默认使用指针  
可以使用grabWidget()和grabWindow()将QPixmap的图像绘制到目标上  


### QBitmap

是QPixmap的子类，但是色深为1，即只有黑白色，占用空间小  
适合光标 笔刷等图像  
可以使用QPixmap::isQBitmap()函数判断  

### QImage

可以进行像素级的访问操作  

```cpp
QImage image(3, 3, QImage::Format_RGB32);
QRgb value;

value = QRgb(189, 149, 39);
image.setPixel(1, 1, value);//设置(1,1)像素的rgb值
```

### QPicture

与平台无关，可以使用在svg pdf ps 打印机或屏幕等多种设备上  
可以记录QPainter命令  

```cpp
QPicture picture;
QPainter painter;

painter.begin(&picture);//在picture上绘制
painter.drawEllipse(10, 20, 80, 70);
painter.end();//绘制完成

picture.save("drawing.pic");//保存
```

```cpp
QPicture picture;
QPainter painter;

picture.load("drawing.pic");
painter.begin(&myImage);               
painter.drawPicture(0, 0, picture);//绘制picture
painter.end(); 
```

## Graphics View Framework

提供了一种借口来管理大量的自定义2D图像元素并交互  
还提供了将这些元素进行可视化显示的观察组件，支持缩放与旋转  

该框架还提供了一套完整的**事件体系**与元素交互，支持键盘 鼠标事件等  

它是一个基于元素（item）的MV架构，分为三个部分：元素item 场景scene 和视图view  
首先创建一个场景，然后创建一个直线对象和一个多边形对象，在使用场景的add函数将对象添加到场景中，最后通过视图来观察  


### MV架构

M:model 模型，添加的各种对象  
V:view 视图，观察对象的视口，一个模型可以从多个视图不同角度观察  

QGraphicsScene是场景，允许我们添加图形，相当于整个世界  
QGraphView是视口，相当于照相机的取景框，可以是全景也可以是场景的一部分  
QGraphiceItem是图形元素  

```cpp
QGraphicsScene scene;
scene.addLine(0, 0, 150, 150);

QGraphiceView view(&scene);
view.setWindowTitle("viewTitle");
view.resize(500, 500);
view.show();
```

---
## 贪吃蛇

---
## 文件

文件操作类继承于一个父类QIODevice  

### QIODevice

所有IO设备类的父类，提供字节块的通用操作和接口  

子类有：  
- QBuffer读写QByteArray  
- QProcess运行外部程序，处理进程间的通讯  
- QFileDevice文件类的通用操作  
  - QFile访问本地文件或嵌入资源  
    - QTemporaryFile创建和访问本地的临时文件  
- QAbstractSocket所有套接字的父类  
  - QTcpSocket TCP协议  
    - QSslSocket 
  - QUdpSocket UDP报文  

#### 顺序访问

数据只能访问一遍，从第一个字节开始到最后  
不能返回读上一个字节  
- QProcess  
- QTcpSocket  
- QUdpSocket  
- QSslSocket  

#### 随机访问

可以访问**任意位置任意次数**  
可以使用`QIODevice::seek()`来重新定位文件访问指针  

### QFile

提供了从本地文件中读取和写入数据的能力  
对文件的公共操作放在了**QFileDevice类**中  

构造参数常为文件路径，也可以使用`setFileName()`来修改  
路径使用正斜杠`/`分割，在不同系统上会自动转换如`C:/Windows`在Windows平台上同样可以使用  

- QFile提供了文件操作如打开，关闭，刷新等  
- 数据读写使用QDataStream或QTextStream  
- 数据读写还可以使用QIODevice的read() readLine() readAll() write()等函数  
- 文件本身的信息如文件名，目录名等是通过QFileInfo获取  

```cpp
//创建文件对象，QDir::currentPath()可以获得执行路径
QFile file("in.txt");

//打开文件，只读 + 文本
if(!file.open(QIODevice::ReadOnly | QIODevice::Text))
{
    qDebug() << "open failed";
}
else
{
    while (!file.atEnd())
    {
        qDebug << file.readLine();
    }
}


QFileInfo info(file);

qDebug() << info.isDir();
qDebug() << info.isExecutable();
qDebug() << info.baseName();//文件名
qDebug() << info.completeBaseName();
qDebug() << info.suffix();//后缀名
qDebug() << info.completeSuffix();
```

---
## QDataStream 二进制流读写

### 二进制流

数据流是一种二进制流，它不依赖于操作系统  CPU 或者字节顺序等等  

写入：

```cpp
QFile file("file.dat");

if(file.open(QIODevice::WriteOnly))
{
    QDataStream out(&file);
    
    out << QString("the answer is");
    out << (qint32)42;//使用qint32是为了保证在不同平台和编译器上都有一样的行为

    file.flush();//数据只有在文件关闭时才会写入，flush可以在不关闭的情况下写入文件
    file.close();
}
```

读取：

```cpp
QFile file("file.dat");

if(file.open(QIODevice::ReadOnly))
{
    QDataStream in(&file);
    QString str;
    qint32 a;

    //数据的读取顺序必须按照写入的顺序来，否则会出异常甚至崩溃
    in >> str >> a;

    file.close();
}
```


### 魔术数字和版本

因为二进制读取顺序要和写入顺序完全一致，因此不同版本保存的文件顺序若有差异则会难以处理  
必须使用一种机制保证不同版本之间的一致性  

魔术数字就是二进制输出常用的技术  
魔术数字写在文件开头，象征一个特征码，在读取时先检查这个特征码，如果与预先设置的不同就停止读取  
一般是32位无符号整型数字如`(quint32)0xA0B0C0D0`  


魔术数字只能判断该文件是否是合法的可读文件，为了解决版本之间的差异还要加版本号  

写入：  

```cpp
QFile file("file.dat");
file.open(QIODevice::WriteOnly);

QDataStream out(&file);
 
// 写入魔术数字和版本
out << (quint32)0xA0B0C0D0;
out << (qint32)123; 
out.setVersion(QDataStream::Qt_4_0);
 
// 写入数据
out << lots_of_interesting_data;
```

读取：
```cpp
QFile file("file.dat");
file.open(QIODevice::ReadOnly);
QDataStream in(&file);

// 检查魔术数字
quint32 magic;
in >> magic;
if (magic != 0xA0B0C0D0) 
{
    return BAD_FILE_FORMAT;
}

// 检查版本
qint32 version;
in >> version;

//排除错误的版本号，正确的号[100, 123]
if (version < 100) 
{
    return BAD_FILE_TOO_OLD;
}

if (version > 123) 
{
    return BAD_FILE_TOO_NEW;
}

//[100, 110]使用Qt_3_2读取
if (version <= 110) 
{
    in.setVersion(QDataStream::Qt_3_2);
} 
else //(110,123]用Qt_4_0读取
{
    in.setVersion(QDataStream::Qt_4_0);
}

// 读取数据
in >> lots_of_interesting_data;
if (version >= 120) {
    in >> data_new_in_version_1_2;
}
in >> other_interesting_data;
```


### 流的游标

```cpp
QFile file("file.dat");
file.open(QIODevice::ReadWrite);

QDataStream stream(&file);
QString str = "the answer is 42";
QString strout;

stream << str;
file.flush();//此时游标在文件末尾


stream.device()->seek(0);//设置游标到文件开头
stream >> strout;
```

---
## QTextStream 文本文件读写

QTextStream可以操纵文本文件  
XML HTML虽然也是文本文件可以有QTextStream生成，但是Qt有更方便的类处理它们  

QTextStream会自动将Unicode编码和换行符自动与操作系统进行匹配  
其以16位的QChar作为基础的数据存储单位  

```cpp
QFile data("file.txt");

if (data.open(QFile::WriteOnly | QIODevice::Truncate)) 
{
    QTextStream out(&data);
    out << "The answer is " << 42;
}
```

### 打开模式

枚举值 | 描述
- | -
QIODevice::NotOpen | 未打开
QIODevice::ReadOnly | 只读
QIODevice::WriteOnly | 只写
QIODevice::ReadWrite | 读写
QIODevice::Append | 追加至末尾
QIODevice::Truncate | 重写 <br>写入时清除旧数据 <br>游标位于开头
QIODevice::Text | 读取：换行符-> \n <br>写入：换行符->本地格式（如\r\n)
QIODevice::Unbuffered | 忽略缓存


### 编码

文本文件在读取的时候，通常会一次读一行`readLine()`或读取全部`readAll()`  
之后再对读取的QString对象处理  

默认编码是Unicode如果要使用另外的可以`stream.setCodec("UTF-8")`  

```cpp
out << bin << 1234;//使用2进制输出

//输出带有前缀 全部字母大写的 十六进制（0XBC614E）
out << showbase << uppercasedigits << hex << 1234567890;
```

也可以直接输出到QString

```cpp
QString str;
QTextStream(&str) << oct << 31 << dec << 25;
```

---
## 存储容器

常用的数据结构，类似STL  
容器类都不继承QObject，提供隐式数据共享，与平台无关  

### 顺序存储容器

#### QList<T>

基于数组实现的列表  
可以基于索引快速访问，可以使用`QList::append()`和`QList::prepend()`添加元素  
`QList::insert()`在中间插入
对于字符串有QStringList，它继承自QList<QString>

#### QLinkedList<T>

基于QList，使用遍历器，不基于索引，在插入时优于QList  

#### QVector<T>

在内存中的**连续区域**存储一系列值

#### QStack<T>

QVector的子类，栈  
有push() pop() top()函数  

#### QQueue<T>

QList子类，队列  
有enqueue() dequeue() head()函数

### 关联容器

#### QSet<T>

单值的数学集合，快速查找

#### QMap<Key, T>

字典  
每个键与一个值关联，QMap以键的顺序存储数据  
如果顺序无关，则QHash性能更佳  

#### QMultiMap<Key, T>

QMap的子类，提供多值映射，即一个键可以对应多个值  

#### QHash<Key, T>

与QMap接口几乎相同，但是速度更快，以字母顺序存储数据  

使用QMap或QHash，键的类型必须提供额外的辅助函数  
QMap的键必须提供`operator<()`重载  
QHash的键必须提供`operator==()`重载和一个名字是`qHash()`的全局函数  

#### QMultiHash<Key, T>

多值散列

### 容器嵌套

所有的容器都可以嵌套  
`QMap<QString, QList<int> >`  
注意最后的两个`> >`一定要用空格隔开，不然会理解为输入重定向运算符

### 可赋值数据类型

有默认构造函数 拷贝构造函数 赋值运算符的类型  
基本上大多数据类型都是可赋值数据类型  

QObject及其子类不是，因此容器存储只能使用指针`QList<QWidget *>`  


---
## 遍历容器

对用容器的常用操作  

### Java风格

方便但是不如STL高效  




### STL风格

兼容Qt与STL通用算法  
只读访问比读写访问快

容器 | 只读遍历器 | 读写遍历器
- | - | -
QList<T> <br> QQueue<T> | QList<T>::const_iterator | QList<T>::iterator
QLinkedList<T> | QLinkedList<T>::const_iterator | QLinkedList<T>::iterator
QVector<T> <br> QStack<T> | QVector<T>::const_iterator | QVector<T>::iterator
QSet<T> | QSet<T>::const_iterator | QSet<T>::iterator
QMap<Key, T> <br> QMultiMap<Key, T> | QMap<Key, T>::const_iterator | QMap<Key, T>::iterator
QHash<Key, T> <br> QMultiHash<Key, T> | QHash<Key, T>::const_iterator | QHash<Key, T>::iterator


`++`运算符可以移动到下一元素  
`*``可以获取遍历器指向的元素  

```cpp
QList<QString> list;
list << "A" << "B" << "C" << "D";

QList<QString>::iterator i;
for(i = list.begin(); i != list.end(); ++i)
{
    *i = (*i).toLower();
}

QList<QString>::const_iterator i;
for(i = list.constBegin(); i != list.constEnd(); ++i)
{
    qDebug() << *i;//i是遍历器，*i是这个元素
}
```

STL遍历器直接指向**元素本身**  
`begin()`函数指向第一个元素遍历器  
`end()`返回**最后一个元素之后的元素**的遍历器，实际上是一个**非法位置**  


```cpp
QMap<int, int> map;

QMap<int, int>::const_iterator i;
for(i = map.constBegin(); i != map.constEnd(); ++i)
{
    qDebug() << i.key() << i.value();
}
```

由于有隐式数据共享，一个函数返回集合中元素的值也不会有很大的代价  
Qt API中有不少以值的形式返回QList或QStringList的函数  
