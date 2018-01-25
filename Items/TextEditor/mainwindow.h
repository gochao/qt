#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QMdiArea>
#include "editor.h"

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = 0);
    ~MainWindow();



private:
    /*---------------- ----------------*/
    QMdiArea * mdiArea;


    /*---------------- ----------------*/
    Editor* createEditor();
    Editor* getActiveEditor();
    QMdiSubWindow* findSubWindow(const QString filePath);
    void updateMenus();


    /*----------------动作----------------*/
    QAction * actionOpen;//打开文件
    QAction * actionNew;//新建文件
    QAction * actionSave;//保存文件
    QAction * actionSaveAs;//另存为文件
    QAction * actionExit;//退出
    QAction * actionUndo;//撤销
    QAction * actionRedo;//恢复
    QAction * actionCut;//剪切
    QAction * actionCopy;//复制
    QAction * actionPaste;//粘贴
    QAction * actionClose;//关闭
    QAction * actionCloseAll;//关闭所有窗口
    QAction * actionTile;//平铺
    QAction * actionCascade;//层叠
    QAction * actionNext;//下一个
    QAction * actionPrevious;//上一个
    QAction * actionAbout;//关于


    /*----------------初始化----------------*/
    void initUI();//初始化界面
    void initAction();//初始化Action
    void initMenu();//创建菜单
    void initWidget();

private slots:
    /*----------------槽函数----------------*/
    void newFile();
    void openFile();
    //void saveFile();

};

#endif // MAINWINDOW_H
