# QtQuick

[参考资料:QtQuick核心编程](https://book.douban.com/subject/26274183/)

## 目录
[TOC]

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