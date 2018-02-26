# QtQuick

[参考资料:QtQuick核心编程](https://book.douban.com/subject/26274183/)

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