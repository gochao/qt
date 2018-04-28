# QtQuick

[参考资料:QtQuick核心编程](https://book.douban.com/subject/26274183/)

## 目录
[TOC]

## QML基础

QML实现并扩展了ECMAScript  
Qt Quick是开发QML的标准库  

### 对象

QML文件名为.qml的文本文件  

```
import QtQuick 2.2

Rectangle {
    width:320;
    height:480;

    Image{
        source:"img/1.jpg";
        anchors.centerIn:parent;
    }
}
```

### 表达式

```
Rectangle{
    width:23*10;
    height:6*80;
    color:"#121212"
}

Button {
    text:"Quit";
    style: ButtonStyle {
        background: Rectangle {
            border.width: control.activeFocus ? 2:1;
        }
    }
}
```

以上将border.width和控件属性联系起来  

引用另一个对象还可以使用id值

```
Button {
    id: openFile;
}

Button {
    id: quit;
    anchors.left = openFile.right;
}
```

### 属性

小写开头,驼峰命名 implicitWidth

有以下几种类型:  
- 基本类型,由QML提供  
- Qt Quick提供  
- C++

int real double string list font等  
属性有类型检测,要使用匹配的类型  

id属性是唯一的,一个qml文件中不重复  

list属性[],元素由","隔开,只能包含QML对象,不能包含字面量如 8, true等  

## main.cpp分析

```
QGuiApplication app(argc, argv);

QQmlApplicationEngine engine;//QML引擎
engine.load(QUrl(QStringLiteral("qrc:///main.qml")));//引擎启动主qml

return app.exec();
```

## 基本元素

### Rectangle

可以代替window作为根对象  
width height指定宽和高  
color:填充颜色,设置为transparent则不填充  
gradient:渐变色填充  

### 颜色

参考 QMLBasic Type:color
可以使用名字指定颜色:blue red  
使用"#RRGGBB" 或 "#AARRGGBB"
使用Qt.rgba() Qt.lighter()等指定颜色  
#### 渐变

Gradient指定

```js
Rectangle {
    width: 100;
    height: 100;
    gradient: Gradient {
        GradientStop {position:0.0; color:"#202020";}
        GradientStop {position:0.33; color: "blue"}
        GradientStop {position:1.0; color:"#FFFFFF";}
    }
}
```

### Item

所有可视元素的基类,定义了绘图大部分通用的属性,如x,y,width,height,anchoring,key,z(叠加顺序), opacity(透明度)

clip属性根据自己的位置和大小来裁剪它自己以及孩子的显示范围,为true则child不能超出parent  
其他属性还有:  
scale smooth anchors antialiasing enabled visible state states children transitions等  
详细信息可查看Item帮助  

### 锚布局

item的7条线:  
left horizontaCenter top bottom right verticalCenter baseline  

其中baseline是文字的低端线,非文字与top一致

对齐时还可以指定间隔:topMargin...

```js
import QtQuick 2.2

Rectangle {
    width: 300;
    height: 200;

    Rectangle {
        id: rect1;
        anchors.left: parent.left;
        anchors.leftMargin: 20;
        anchors.top: parent.top;
        anchors.topMargin: 20;
    }

    Rectangle {
        anchors.fill: parent;//全部填充到父组件

        Rectangle {
            anchors.centerIn: parent;
        }
    }
}
```

### 响应按键

所有Item都可以自己响应按键  
通过附加属性Keys来处理按键的信号  
还有个类型为KeyEvent,名字是event的参数,包含按键的详细信息,一个按键被处理,event.accepted设置为true防止继续传递  
```js
Rectangle {
    width: 300;
    height: 200;
    focus: true;
    Keys.enabled = true;
    Keys.onEscapePressed: Qt.quit();
    Keys.onBackPressed: Qt.quit();
    Keys.onPressed: {
        switch(event.key){
        case Qt.Key_0:
        case Qt.Key_1:
        case Qt.Key_2:
        case Qt.Key_3:
        case Qt.Key_4:
        case Qt.Key_5:
        case Qt.Key_6:
        case Qt.Key_7:
        case Qt.Key_8:
        case Qt.Key_9:
            event.accepted = true;
            keyView.text = event.key - Qt.Key_0;
            break;
        }
    }

    Text {
        id: keyView;
        anchors.centerIn: parent;
    }
}
```

### Text

显示纯文本或者富文本  
属性: font text color elide textFormat wrapMode horizontalAlignment vericalAlignment  

textFormat默认使用Text.AutoText检测文本类型是纯文本还是富文本

```js
Rectangle {
    width: 320;
    height: 200;
    Text {
        wrapMode: Text.WordWrap;
        font.bold: true;
        font.pixelSize: 24;
        text: "Hello text";
    }
}
```

### Button

属性:  
- text 文字  
- checkable 可选,checked保存状态  
- iconName 图标名字,如果有对应的资源就优先使用
- iconSource URL方式指定icon位置  
- isDefault 是否为默认按钮  
- pressed 保存按钮按下状态  
- menu 按钮设置菜单  
- action 
- activeFocusOnPress  
- style 按钮风格ButtonSytle  

#### ButtonStyle

需要使用 QtQuick.Controls.Sytles 1.x  
有background control label三个属性  

- background Component类型,绘制Button背景  
- label Component类型,定制文本  
- control属性指向使用ButtonStyle的按钮对象  

```js
import QtQuick 2.2
import QtQuick.Controls 1.2
import QtQuick.Controls.Sytles 1.2

Button {
    style: ButtonStyle {
        background: Rectangle {
            implicitWidth: 70;
            implicitHeight: 25;
            border.width: control.pressed ? 2 : 1;
            border.color: control.hovered ? "green" : "#888888";
        }
    }
}
```

### Image

显示Qt支持的静态图片  
width height 设置图元的大小,否则使用图片本身的尺寸  
fillMode设置填充模式:  
- 拉伸(Image.Stretch) 
- 等比缩放(Image.PreserveAspectFit)  
- 等比缩放,最大化填充Image必要时裁剪图片(Image.PreserveAspectCrop)  
- 平铺 (ImageTile)

默认阻塞加载图片,asynchronous属性开启异步加载模式  
也可以从网络加载图片,此时会自动使用异步加载,加载完毕后status会更新Image.Ready  

### BusyIndicator

显示一个等待图元

```js
BusyIndicator {
    id: busy;
    running: true;
    anchors.centerIn: parent;
    z: 2;
}
```

### FileDialog 

visible属性默认为false,使用open()设置为true  
selectExisting 选择已有的,false可以提供用户创建文件或文件夹  
selectFolder 选择文件还是文件夹  
selectMultiple 默认单选
nameFilters 设定一个过滤器列表 selectedNameFilter保存用户选择的过滤器  
modality 默认Qt.WindowModal

fileUrl保存文件路径,多个文件则由fileUrls返回列表  

```js
FileDialog {
    id: fileDialog;
    nameFilters: ["Image(*.jpg)", "Bitmap(*.bmp)"];
    selectedNameFilter: "Image(*.jpg)";
    selectMultiple: true;
    onAccepted: {
        imageViewr.source = fileDialog.fileUrls[0];
        var imageFile = new String(filDialog.fileUrls[0]);
    }
}
```

## ECMAScript

JavaScript的实现包含三个不同的部分:  
- 核心(ECMAScript)  
- 文档对象模型(DOM)  
- 浏览器对象模型 (BOM)  

ECMAScript为不同的宿主环境提供脚本编程能力  
浏览器只是一个宿主环境,QML也是其中之一  
其他语言可以实现ECMAScript来作为功能基础,又可以被扩展,包含宿主环境的新特性  

### 语法基础

变量区分大小写  
若类型,使用var  
分号可有可无  
注释与c一致  
代码块为花括号  

### 原始类型

Undefined Null Boolean Number String为字面量,可以通过typeof来判断一个值的类型,如果为原始类型返回类型名字,若是引用类型,则返回"object"  

#### Undefined

声明变量未初始化时的默认值  

#### Null

引用变量初始值  

#### Number

32位整数或者64位浮点数  
数字介于Number.MAX_VALUE最小值是Number.MIN_VALUE 定义外边界  

当数字大于边界时变为Number.POSITIVE_INFINITY
(正无穷大)和Number.NEGATIVE_INFINITY(负无穷大)

使用isFinit()判断一个数是否有穷  
非数是NaN 判断非数使用isNan()方法  

#### String

使用双引号或单引号表示  
同样包含转义字符  

### 类型转换

Boolean Number String有toString()方法转换为字符串  

parseInt()和parseFloat()可以把非数字转换成数字,且只能用于String类型的转换,其他类型转换变为NaN

#### 强制类型转换  

- Boolean(value):非空字符串 非0数字或对象  
- Number(value):自动调用parse函数  
- String(value)  

### 对象

#### Object

所有类的基类  
属性:  
- constructor:指向创建对象的函数  
- prototype: 对象原型的引用  
方法:  
- hasOwnProperty(property):判断对象是否含有某个属性  
- isPrototypeOf(object): 判断该对象是否为另一个对象的原型  
- propertyIsEnumerable(property)判断给定的属性是否可以枚举  
- toString()  
- valueOf()适合该对象的原始值  


#### 动态增加属性  

```js
var person = new Object(0;);
person.name = "zz";
person.year = 20;//添加Object中没有的属性  
```

#### 动态添加方法  

```js
person.printInfo = function printInfo() {
    console.log("info");
}

person.printInfo();
```

#### 下标访问  

```js
console.log(person["name"]);
person["printInfo"]();
```

#### for...in枚举属性

```js
for (var prop in person) {
    console.log(prop. ",", person[prop]);
}
```

#### 对象的字面量表示法

```js
var person = {
    "name": "zz";
    "year": 20;
}
```

得到新的对象,JSON的核心语法  

### String

```js
var str = new String("I am a string");
console.log(str.length);//长度  

console.log(str[0]);
console.log(str.charAt(2));//访问单个字符  

console.log(str.indexOf("am"))//查找子串,失败返回-1

str.search();
str.match();//返回存放所有子串的数组

//字符串连接
str1 + str2;
str1.concat("newS");

//提取子串
var str = new String("I like QML");
str.slice(-3);//QML
str.slice(2, 6);//like

//大小写转换
toLowerCase();
toLocaleLowerCase();
toUpperCase();
toLocaleUpperCase();

//QML扩充
var exp = "%1 < %2 = %3";
exp.arg(7).arg(8).arg("true");
```

### 正则表达式

### Array

大小可以动态变化,元素类型可以不同  

```js
var a = new Array();
var a = new Array(10);
var a = new Array(10, 6, 3);

a.push(20);
a.unshift(1);
a.pop();
a.sort();
join();//合并为一个字符串
```

#### Math

全局对象,不需要new构造

```js
var pi = Math.PI;
```

#### Date

```js
var today = new Date();
getDate();//1-31
getDay();//0-6
getMonth();//0-11
getFullYear();//xxxx
getTime();//时间戳
```


### 函数

#### 语法

```js
function quit {
    Qt.quit();
}

function showError(msg) {
    console.log(msg);
}
```

函数默认都有返回值,没有return则返回undefined


## 事件处理

### 键盘

Keys对象处理按键事件  
有针对特定按键的信号,returnPressed,也有普通的pressed和released信号  

KeyEvent代表一个按键事件,event.accepted应该被设置为true,以免继续传递  

forwardTo对应一个列表类型,一次传递按键事件给列表内的对象,如果某个对象接受了,就不会继续传递下去  

priority属性设置优先级,在Item默认处理方法之前处理按键和在Item之后处理按键.区别是可以自己处理后accept  

想让某个元素处理按键,就要传递焦点focus  

实例:可移动文本  

```js
import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Window 2.3

Window {
    visibility: "Maximized"
    visible: true;

    Rectangle {
        anchors.fill: parent;
        color: "gray";

        focus: true;
        Keys.enabled: true;
        Keys.onEscapePressed: {
            Qt.quit();
        }
        Keys.forwardTo: [moveText, likeQt];

        Text {
            id: moveText;
            x: 20;
            y: 20;
            width: 200;
            height: 30;
            text: "Moving Text";
            color: "blue";
            font: {bold:true; pixelSize: 100;}
            Keys.enabled: true;
            Keys.onPressed: {
                switch(event.key){
                case Qt.Key_Left:
                    x -= 10;
                    break;
                case Qt.Key_Right:
                    x += 10;
                    break;
                case Qt.Key_Up:
                    y -= 10;
                    break;
                case Qt.Key_Down:
                    y += 10;
                    break;
                default:
                    return;
                }
                event.accepted = true;
            }
        }

        CheckBox {
            id: likeQt;
            text: "Like Qt Quick";
            anchors.left: parent.left;
            anchors.bottom: parent.bottom;
            z: 1;
        }
    }
}

```

### 定时器

Timer代表定时器  响应triggered()信号使用  
interval指定定时周期 默认1000毫秒  
repeat设定周期触发  
running 设置可用  
triggeredOnStart开始时立即触发一次默认false  

方法有 start() stop() restart()  

倒计时实例:  

```js
import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Window 2.3

Window {
    visibility: "Maximized"
    visible: true;

    Text {
        id: txt;
        anchors.centerIn: parent;
        font.family: "微软雅黑";
        font.pixelSize: 200;
        property int sec: 10;
    }

    Button {
        id: btn;
        text: "Start";
        anchors.horizontalCenter: txt.horizontalCenter;
        anchors.top: txt.bottom;
        anchors.topMargin: 50;

        onClicked: {
            txt.sec = 10;
            timer.restart();
        }
    }

    Timer {
        id: timer;
        interval: 1000;
        repeat: true;

        onTriggered: {
            if (txt.sec > 1)
            {
                txt.sec -= 1;
                txt.text = txt.sec.toString();
            }
            else
            {
                txt.text = "Clap Now!";
                timer.stop();
            }
        }
    }
}

```


## 组件与动态对象


## 信号槽

### 连接QML类型的已知信号

```js
import QtQuick 2.2
import QtQuick.Controls 1.2

Rectangle {
    width:320;
    height: 240;
    color: "gray";

    Button {
        text: "Quit";
        anchors.centerIn: parent;
        onClicked: {
            Qt.quit();
        }
    }
}
```

#### 信号处理器

- 处理信号的槽函数是以`on[SignalName]`包含的代码块  
- 只能在定义的地方使用，不能在其他地方调用  
- 处理元素内部的信号，而不能处理其他对象发出的信号  

#### 附加信号处理器

- 附加属性和附加信号处理器是QML的语法概念，由附加类型实现并提供  
- 对象的普通属性是对象自身或基类提供的，而附加属性则不是  

```js

Item {
    width: 100;
    height: 100;
    focus: true;

    Keys.enabled:false;//附加属性
    Keys.onReturnPressed: console.log("pressed");//附加信号处理器
}
```

在上述例子中在一个对象内使用了其他的对象属性和信号处理器，这里用来处理键盘信号  

```js
Rectangle {
    Component.onCompleted: console.log();//初始化
    Component.onDestruction: console.log();//反初始化
}
```

#### Connections

- 信号处理器和附加信号处理器都是在元素内部实现的  
- Connections对象可以创建一个到QML信号的连接  
- 使用场景（包括但不限于）  
  - 一个信号连接到多个对象  
  - 在发出信号的对象作用域之外连接  
  - 发射信号的对象不在QML定义（C++导出）  

```js
Rectangle{
    width: 1027;
    height: 768;

    Text {
        id: txt1;
        text: "text 1";
        font.pointSize: 30;
        anchors.top: parent.top;
    }

    Text {
        id: txt2;
        text: "text 2";
        font.pointSize: 30;
        anchors.bottom: parent.bottom;
    }

    Button {
        id: btn;
        text: "click";
        anchors.centerIn: parent;
    }

    Connections {
        target: btn;//信号发送对象

        //发送的信号 及其处理方式
        onClicked: {
            txt1.color = Qt.rgba(Math.random(), Math.random(), Math.random(), 1);
            txt2.color = Qt.rgba(Math.random(), Math.random(), Math.random(), 1);
        }
    }

}
```

对于对象的属性若帮助文档查不到信号，可以查看源文件`xxx\mingw\include\QtQuick\xxxx\private\xxx.h`中声明的函数  
Q_PROPERTY声明的就是属性，属性后面有NOTIFY字样的就是可以与改属性绑定的信号  

### 自定义信号

自定义的类型信号需要自己添加  

下面的例子是通过点击不同的小方块来切换文字的颜色  

```js
Rectangle{
    width: 1027;
    height: 768;
    color: "#C0C0C0";

    Text {
        id: coloredText;
        text: "text";
        font.pointSize: 100;
        anchors.centerIn: parent;
    }

    //可重复使用的组件
    Component {
        id: colorComponent;
        Rectangle{
            id: colorPicker;
            width: 100;
            height: 100;
            signal colorPicked(color clr);
            MouseArea {
                anchors.fill: parent;
                onPressed: colorPicker.colorPicked(colorPicker.color);
            }
        }
    }

    Loader {
        id: redLoader;
        anchors.left: parent.left;
        sourceComponent: colorComponent;
        onLoaded: {
            item.color = "red";
        }
    }

    Loader {
        id: blueLoader;
        anchors.right: parent.right;
        sourceComponent: colorComponent;
        onLoaded: {
            item.color = "blue";
        }
    }

    Connections {
        target: redLoader.item;
        onColorPicked: {
            coloredText.color = clr;
        }
    }

    Connections {
        target: blueLoader.item;
        onColorPicked: {
            coloredText.color = clr;
        }
    }

}
```

## C++混合编程

QML适用于快速的界面编辑，复杂逻辑运算一般还需要C++实现，因此需要在QML中使用C++  
同时C++也可以使用QML对象  
本部分使用的示例是一个显示实时时间，同时会自动变色的小程序  

### QML中使用C++

在QML中使用C++也有两种方式：  
- C++中实现一个类，注册为QML的一个类型，**在QML中创建对象**  
- **C++中构造对象**，将这个对象设置为QML的上下文属性  

无论哪种方法对于C++类都有特殊的要求  

#### 定义可导出的C++类

##### 前提条件

- 从QObject或其派生类继承  
- 使用QObject宏  

目的是使用Qt的元对象系统，与信号槽类似  

##### 注册成员函数

修改内容：Q_INVOKEABLE宏：在成员函数返回类型前修饰，可以让该函数被元对象系统调用  
信号槽的函数不需要添加宏，因为信号槽机制已经被元对象系统特殊处理过了  

```cpp
class ColorMaker : public QObject
{
    Q_OBJECT
public:
    explicit ColorMaker(QObject *parent = nullptr);

    Q_INVOKABLE GenerateAlgorithm algorithm() const;
    Q_INVOKABLE void setAlgorithm(GenerateAlgorithm algorithm);

signals:
     void colorChanged(const QColor & color);
    void currentTime(const QString & strTime);

public slots:
    void start();
    void stop();
};
```

##### 注册枚举

使用Q_ENUMS宏将枚举类型GenerateALgorithm包装

```cpp
class ColorMaker : public QObject
{
    Q_OBJECT
    Q_ENUMS(GenerateAlgorithm)

public:
    explicit ColorMaker(QObject *parent = nullptr);

    enum GenerateAlgorithm{
        RandomRGB,
        RandomRed,
        RandomGreen,
        RandomBlue,
        LinearIncrease
    };

    Q_INVOKABLE GenerateAlgorithm algorithm() const;
    Q_INVOKABLE void setAlgorithm(GenerateAlgorithm algorithm);

signals:
     void colorChanged(const QColor & color);
    void currentTime(const QString & strTime);

public slots:
    void start();
    void stop();
};
```

##### 注册属性

Q_PROPERTY宏可以在QML中访问，修改属性 或当属性变化时发射指定信号  
它的使用比较复杂，参数多达10个  

例子:  

```cpp
Q_PROPERTY(int x READ x)//类型为int 名字为x的属性，通过方法x()来访问  
Q_PROPERTY(QString text READ text WRITE setText NOTIFY textChanged)//类型为int 名字为text的属性，通过方法text()来访问,通过方法setText()来修改, 其值变化时触发textChanged信号
```

- READ：如果属性不是MEMBER标记，那么就必须有READ标记声明一个读取函数，返回该属性  
- WRITE：可选，声明一个没有返回值的函数，参数是当前属性，用于修改属性值  
- NOTIFY：可选，管理一个信号（类中声明过的），当属性值改变时触发被关联的信号，参数一般是定义的属性  

现在给ColorMaker添加属性

```cpp
class ColorMaker : public QObject
{
    Q_OBJECT
    Q_ENUMS(GenerateAlgorithm)
    Q_PROPERTY(QColor color READ color WRITE setColor NOTIFY colorChanged)
    Q_PROPERTY(QColor timeColor READ timeColor)

public:
    explicit ColorMaker(QObject *parent = nullptr);

    enum GenerateAlgorithm{
        RandomRGB,
        RandomRed,
        RandomGreen,
        RandomBlue,
        LinearIncrease
    };

    QColor color() const;
    void setColor(const QColor & color);
    QColor timeColor() const;

    Q_INVOKABLE GenerateAlgorithm algorithm() const;
    Q_INVOKABLE void setAlgorithm(GenerateAlgorithm algorithm);

signals:
     void colorChanged(const QColor & color);
    void currentTime(const QString & strTime);

public slots:
    void start();
    void stop();

protected:
    void timerEvent(QTimerEvent * e);

private:
    GenerateAlgorithm m_algorithm;
    QColor m_currentColor;
    int m_nColorTimer;
};
```

至此对于C++类的头文件已经全部修改完成  

##### 实现代码

```cpp
#include "ColorMaker.h"
#include <QTimerEvent>
#include <QDateTime>


ColorMaker::ColorMaker(QObject *parent)
    : QObject(parent)
    , m_algorithm(RandomRGB)
    , m_currentColor(Qt::black)
    , m_nColorTimer(0)
{
    qsrand(QDateTime::currentDateTime().toTime_t());
}


QColor ColorMaker::color() const
{
    return m_currentColor;
}


void ColorMaker::setColor(const QColor & color)
{
    m_currentColor = color;
    emit colorChanged(m_currentColor);
}


QColor ColorMaker::timeColor() const
{
    QTime time = QTime::currentTime();
    int r = time.hour();
    int g = time.minute() * 2;
    int b = time.second() * 4;
    return QColor::fromRgb(r, g, b);
}

ColorMaker::GenerateAlgorithm ColorMaker::algorithm() const
{
    return m_algorithm;
}


void ColorMaker::setAlgorithm(GenerateAlgorithm algorithm)
{
    m_algorithm = algorithm;
}

void ColorMaker::start()
{
    if(m_nColorTimer == 0)
    {
        m_nColorTimer = startTimer(1000);
    }
}

void ColorMaker::stop()
{
    if(m_nColorTimer > 0)
    {
        killTimer(m_nColorTimer);
        m_nColorTimer = 0;
    }
}

void ColorMaker::timerEvent(QTimerEvent *e)
{
    if(e->timerId() == m_nColorTimer){
        switch (m_algorithm) {
        case RandomRGB:
            m_currentColor.setRgb(qrand()%255, qrand()%255, qrand()%255);
            break;
        case RandomRed:
            m_currentColor.setRed(qrand()%255);
            break;
        case RandomBlue:
            m_currentColor.setBlue(qrand()%255);
            break;
        case RandomGreen:
            m_currentColor.setGreen(qrand()%255);
            break;
        case LinearIncrease:
            int r = (m_currentColor.red() + 10) % 255;
            int g = (m_currentColor.blue() + 10) % 255;
            int b = (m_currentColor.green() + 10) % 255;
            m_currentColor.setRgb(r, g, b);
            break;
        }

        emit colorChanged(m_currentColor);
        emit currentTime(QDateTime::currentDateTime().toString("yyyy-MM-dd hh:mm:ss"));
    }
    else{
        QObject::timerEvent(e);
    }
}

```

#### C++类注册为QML类

修改好的C++类还不能直接在QML中使用，还需以下几步：  
- 注册QML类型  
- 在QML中导入类型  
- 创建实例并使用  

##### 注册QML类型

注册函数有：(#include <QtQml>)  
- qmlRegisterSingletonType() 注册单例  
- qmlRegisterType() 注册非单例  
- qmlRegisterTypeNotAvailable() 注册一个类型来占位  
- qmlRegisterUncreatableType() 注册一个具有附加属性的附加类型  

以qmlRegisterType为例子，有4个参数：  
- uri 包名，避免名字冲突，QtQuick.Controls 就是包名  
- 两个版本号如1.0  
- qmlName为QML中的类名  

main.cpp

```cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QtQml>
#include "ColorMaker.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    qmlRegisterType<ColorMaker>("cpp", 1, 0, "ColorMaker");

    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
```

##### QML导入类型

import + 包名 + 版本号  
`import cpp 1.0`  

##### QML中使用

```js
import QtQuick 2.2
import QtQuick.Window 2.0
import QtQuick.Controls 1.4
import cpp 1.0

Window{
    visible: true;
    width: 1024;
    height: 768

    Rectangle{
        anchors.fill: parent;

        Text {
            id: timeTxt;
            anchors.left: parent.left;
            anchors.top: parent.top;
            font.pixelSize: 26;
        }

        ColorMaker{
            id: colorMaker;
        }

        Rectangle{
            id : colorRect;
            anchors.centerIn: parent;
            width: 200;
            height: 200;
            color: "blue";
        }

        Button {
            id: start;
            text: "start";
            anchors.left: parent.left;
            anchors.bottom: parent.bottom;
            anchors.margins: 5;
            onClicked: {
                colorMaker.start();
                console.log("start...");
            }
        }

        Button {
            id: stop;
            text: "stop";
            anchors.left: start.right;
            anchors.bottom: parent.bottom;
            anchors.margins: 5;
            onClicked: {
                colorMaker.stop();
                console.log("stop...");
            }
        }

        Button {
            id: colorAlgorithm;
            text: "Algorithm0";
            anchors.left: stop.right;
            anchors.bottom: parent.bottom;
            anchors.margins: 5;
            onClicked: {
                var algorithm = (colorMaker.algorithm() + 1) % 5;
                colorAlgorithm.text = "Algorithm" + algorithm;
                colorMaker.setAlgorithm(algorithm);
                console.log("setAlgorithm...");
            }
        }

        Button {
            id: quit;
            text: "quit";
            anchors.left: colorAlgorithm.right;
            anchors.bottom: parent.bottom;
            anchors.margins: 5;
            onClicked: {
                Qt.quit();
                console.log("quit...");
            }
        }

        Component.onCompleted: {
            colorMaker.color = Qt.rgba(0, 180, 120, 255);
            colorMaker.setAlgorithm(ColorMaker.RandomRGB);
        }

        Connections {
            target: colorMaker;
            onCurrentTime: {
                timeTxt.text = strTime;
                timeTxt.color = colorMaker.timeColor;
            }
        }

        Connections {
            target: colorMaker;
            onColorChanged: {
                colorRect.color = color;
            }
        }

    }
}
```

#### C++对象到处为QML属性  

将C++类导出为QML类型后，可以在QML中创建实例对象并管理其生命周期  
也可以将C++中创建的对象作为属性传递到QML环境中  

注册属性与注册类不同地方在于注册的过程,在根的上下文属性中设置一个全局可见的属性，这个属性名字为colorMaker， 指向一个new出的对象  
此时new出的对象不会被QML自动收回，需要在合适的时机删除  
另外，由于colorMaker会在load中使用到，因此要在load前添加属性  

`engine.rootContext()->setContextProperty("colorMaker", new ColorMaker);`

```cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QtQml>
#include "ColorMaker.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    //qmlRegisterType<ColorMaker>("cpp", 1, 0, "ColorMaker");

    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty("colorMaker", new ColorMaker);//在此处添加是因为在下一行中load会使用到
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
```

在QML中改动如下  

```js
//import cpp 1.0 没有注册类

//ColorMaker{
//  id: colorMaker;
//}已经创建了对象colorMaker不需要再自己创建

//colorMaker.setAlgorithm(ColorMaker.RandomRGB); 不能直接使用ColorMaker类，可以通过对象使用枚举值如下
colorMaker.setAlgorithm(colorMaker.LinearIncrease)
```

### C++中使用QML

在C++中使用QML要简单的多，因为QML本身就是用C++的类实现的，将QML使用在C++中相当于是降维  

#### 查找QML对象
使用QML中的对象首先要找到它  

QObject对象有parent和objectName，通过这个名字就可以查找  

使用findChild()查找父组件parentWidget中名为“btnClick”类型为“QPushButton”的对象 

```
QPushButton *button = parentWidget->findChild<QPushButton *>("btnClick");
```

使用findChildren()查找父组件parentWidget中名为“widgetName”的所有组件列表

```
QList<QWidget *> widgets = parentWidget->findChildren<QWidget *>("widgetName");
```

#### 使用元对象调用QML对象

元对象系统可以：
- 查询QObject的某个派生类的类名，信号槽，属性，可调用方法等  
- `invokeMethod()`静态方法调用一个对象的信号槽和可调用方法  
- 使用QObject的propetry()方法访问属性，setPropetry()修改属性  

invokeMethod() 使用示例：

```cpp
bool QMetaObjcet::invokeMethod(
    QObjcet * obj,
    const char * member,
    Qt::ConnectionType type,
    QGenericReturnArgument ret,
    QGenericArgument val0 = QGenericArgument(0),
    QGenericArgument val1 = QGenericArgument(),
    QGenericArgument val2 = QGenericArgument(),
    QGenericArgument val3 = QGenericArgument(),
    QGenericArgument val4 = QGenericArgument(),
    QGenericArgument val5 = QGenericArgument(),
    QGenericArgument val6 = QGenericArgument(),
    QGenericArgument val7 = QGenericArgument(),
    QGenericArgument val8 = QGenericArgument(),
    QGenericArgument val9 = QGenericArgument(),
)
```

- 返回布尔值  
  - true：调用成功  
  - false: 对象没有该方法或参数不匹配  
- obj 被调用对象指针  
- member 方法名  
- type 连接类型 Qt::DirectConnection Qt::AutoConnection Qt::QueuedConnection  
- ret 接收返回值, 使用`Q_RETURN_ARG`  
- valx 传递给被调用方法的参数  
  - 最多10个参数  
  - 使用Q_ARG宏构造`Q_ARG(Type, const Type & value)`  

```cpp
//假设某对象有一个槽函数compute(QString, int, double) 返回一个QString对象
QString retVal;
QMetaObject::invokeMethod(
    obj, 
    "compute", 
    Qt::DirectConnection,
    Q_RETURN_ARG(QString, retVal),
    Q_ARG(QString, "sqrt"),
    Q_ARG(int, 42),
    Q_ARG(double, 9.7)
    );
```

#### callQml 示例

qml

```js
import QtQuick 2.2
import QtQuick.Window 2.0
import QtQuick.Controls 1.4

Window{
    objectName: "rootObject";
    visible: true;
    width: 1024;
    height: 768

    Text {
        objectName: "textLabel";
        text: "Hello World";
        anchors.centerIn: parent;
        font.pixelSize: 26;
    }

    Button {
        objectName: "quitButton";
        text: "quit";
        anchors.right: parent.right;
        anchors.bottom: parent.bottom;
    }
}
```


```cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QtQml>
#include <QMetaObject>
#include <QColor>
#include "changeColor.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    //获取根对象
    QObject * root = NULL;
    QList <QObject *> rootObjects = engine.rootObjects();
    int count = rootObjects.size();
    for(int i=0; i<count; i++)
    {
        if(rootObjects.at(i)->objectName() == "rootObject")
        {
            root = rootObjects.at(i);
            break;
        }
    }

    //连接quitButton信号槽
    QObject * quitButton = root->findChild<QObject *>("quitButton");
    if(quitButton)
    {
        QObject::connect(quitButton, SIGNAL(clicked()), &app, SLOT(quit()));
    }

    //改变文字和颜色
    QObject * textLabel = root->findChild<QObject *>("textLabel");
    if(textLabel)
    {
        textLabel->setProperty("color", QColor::fromRgb(0, 0, 255));
        textLabel->setProperty("text", "changed!");
        QMetaObject::invokeMethod(textLabel, "doLayout");
    }

    return app.exec();
}
```