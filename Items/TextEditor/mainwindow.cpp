#include "mainwindow.h"
#include <QAction>
#include <QMenuBar>
#include <QFileDialog>
#include <QMessageBox>
#include <QFile>
#include <QMdiSubWindow>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    initUI();
}

MainWindow::~MainWindow()
{
}



void MainWindow::initUI()
{
    initWidget();
    initAction();
    initMenu();
    statusBar();

    setWindowTitle(tr("多文档编辑器"));
    setWindowState(Qt::WindowMaximized);
}


void MainWindow::initAction()
{

    //新建文件
    actionNew = new QAction(tr("新建文件(&N)"), this);
    actionNew->setShortcut(QKeySequence::New);
    actionNew->setStatusTip(tr("新建文件"));
    connect(actionNew, &QAction::triggered, this, &MainWindow::newFile);

    //打开文件
    actionOpen = new QAction(tr("打开文件...(&O)"), this);
    actionOpen->setShortcut(QKeySequence::Open);
    actionOpen->setStatusTip(tr("打开文件"));
    connect(actionOpen, &QAction::triggered, this, &MainWindow::openFile);

    //保存文件
    actionSave = new QAction(tr("保存(&S)"), this);
    actionSave->setShortcut(QKeySequence::Save);
    actionSave->setStatusTip(tr("保存"));
    //connect(actionSave, &QAction::triggered, this, &MainWindow::saveFile);

    //另存为文件
    actionSaveAs = new QAction(tr("另存为...(&A)"), this);
    actionSaveAs->setShortcut(QKeySequence::SaveAs);
    actionSaveAs->setStatusTip(tr("另存为"));

    //退出
    actionExit = new QAction(tr("退出(&X)"), this);
    actionExit->setShortcut(QKeySequence::Quit);
    actionExit->setStatusTip(tr("退出"));

    //撤销
    actionUndo = new QAction(tr("撤销(&U)"), this);
    actionUndo->setShortcut(QKeySequence::Undo);
    actionUndo->setStatusTip(tr("撤销"));
    
    //恢复
    actionRedo = new QAction(tr("恢复(&R)"), this);
    actionRedo->setShortcut(QKeySequence::Redo);
    actionRedo->setStatusTip(tr("恢复"));

    //剪切
    actionCut = new QAction(tr("剪切(&T)"), this);
    actionCut->setShortcut(QKeySequence::Cut);
    actionCut->setStatusTip(tr("剪切"));

    //复制
    actionCopy = new QAction(tr("复制(&C)"), this);
    actionCopy->setShortcut(QKeySequence::Copy);
    actionCopy->setStatusTip(tr("复制"));

    //粘贴
    actionPaste = new QAction(tr("粘贴(&P)"), this);
    actionPaste->setShortcut(QKeySequence::Paste);
    actionPaste->setStatusTip(tr("粘贴"));

    //关闭
    actionClose = new QAction(tr("关闭(&O)"), this);
    actionClose->setStatusTip(tr("关闭"));

    //关闭所有窗口
    actionCloseAll = new QAction(tr("关闭所有窗口(&A)"), this);
    actionCloseAll->setStatusTip(tr("关闭所有窗口"));

    //平铺
    actionTile = new QAction(tr("平铺(&T)"), this);
    actionTile->setStatusTip(tr("平铺"));
    
    //层叠
    actionCascade = new QAction(tr("层叠(&C)"), this);
    actionCascade->setStatusTip(tr("层叠"));
    
    //下一个
    actionNext = new QAction(tr("下一个(&X)"), this);
    actionNext->setShortcut(QKeySequence::NextChild);
    actionNext->setStatusTip(tr("下一个"));
    
    //上一个
    actionPrevious = new QAction(tr("上一个(&V)"), this);
    actionPrevious->setShortcut(QKeySequence::PreviousChild);
    actionPrevious->setStatusTip(tr("上一个"));
    
    //关于
    actionAbout = new QAction(tr("关于(&A)"), this);
    actionAbout->setStatusTip(tr("关于"));
}

void MainWindow::initMenu()
{
    //文件 子菜单
    QMenu * menuFile = menuBar()->addMenu(tr("文件(&F)"));
    menuFile->addAction(actionNew);
    menuFile->addAction(actionOpen);
    menuFile->addSeparator();
    menuFile->addAction(actionSave);
    menuFile->addAction(actionSaveAs);
    menuFile->addSeparator();
    menuFile->addAction(actionExit);
    
    //编辑 子菜单
    QMenu * menuEdit = menuBar()->addMenu(tr("编辑(&E)"));
    menuEdit->addAction(actionUndo);
    menuEdit->addAction(actionRedo);
    menuEdit->addSeparator();
    menuEdit->addAction(actionCut);
    menuEdit->addAction(actionCopy);
    menuEdit->addAction(actionPaste);
    
    //窗口 子菜单
    QMenu * menuWindow = menuBar()->addMenu(tr("窗口(&W)"));
    menuWindow->addAction(actionClose);
    menuWindow->addAction(actionCloseAll);
    menuWindow->addSeparator();
    menuWindow->addAction(actionTile);
    menuWindow->addAction(actionCascade);
    menuWindow->addSeparator();
    menuWindow->addAction(actionNext);
    menuWindow->addAction(actionPrevious);

    //帮助 子菜单
    QMenu * menuHelp = menuBar()->addMenu(tr("帮助(&H)"));
    menuHelp->addAction(actionAbout);

    updateMenus();
}


void MainWindow::initWidget()
{
    mdiArea = new QMdiArea(this);
    setCentralWidget(mdiArea);
    connect(mdiArea, &QMdiArea::subWindowActivated, this, &MainWindow::updateMenus);



}

Editor* MainWindow::createEditor()
{
    Editor * editor = new Editor;
    mdiArea->addSubWindow(editor);

    connect(editor, &QTextEdit::copyAvailable, actionCut, &QAction::setEnabled);
    connect(editor, &QTextEdit::copyAvailable, actionCopy, &QAction::setEnabled);

    connect(editor->document(), &QTextDocument::undoAvailable, actionUndo, &QAction::setEnabled);
    connect(editor->document(), &QTextDocument::redoAvailable, actionRedo, &QAction::setEnabled);

    return editor;
}

void MainWindow::updateMenus()
{
    bool hasEditor = (getActiveEditor() != 0);
    actionSave->setEnabled(hasEditor);
    actionSaveAs->setEnabled(hasEditor);
    actionPaste->setEnabled(hasEditor);
    actionClose->setEnabled(hasEditor);
    actionCloseAll->setEnabled(hasEditor);
    actionTile->setEnabled(hasEditor);
    actionCascade->setEnabled(hasEditor);
    actionNext->setEnabled(hasEditor);
    actionPrevious->setEnabled(hasEditor);


}


Editor* MainWindow::getActiveEditor()
{
    QMdiSubWindow* activeWindow = mdiArea->activeSubWindow();
    if(activeWindow)
    {
        Editor * activeEditor = qobject_cast<Editor *> (activeWindow->widget());
        return activeEditor;
    }
    return 0;
}


QMdiSubWindow* MainWindow::findSubWindow(const QString filePath)
{
    QString canonicalFilePath = QFileInfo(filePath).canonicalFilePath();

    foreach (QMdiSubWindow* subWindow, mdiArea->subWindowList())
    {
        Editor* subEditor = qobject_cast<Editor *>(subWindow->widget());

        if(subEditor->currentFile() == canonicalFilePath)
        {
            return subWindow;
        }
    }

    return 0;
}

/*----------------槽函数实现----------------*/
void MainWindow::newFile()
{
    Editor * editor = createEditor();
    editor->newFile();
    editor->show();
}


void MainWindow::openFile()
{
    QString filePath = QFileDialog::getOpenFileName(this);

    if(!filePath.isEmpty())
    {
        QMdiSubWindow* existingWindow = findSubWindow(filePath);
        if(existingWindow)
        {
            mdiArea->setActiveSubWindow(existingWindow);
        }
        else
        {
            Editor* subEditor = createEditor();
            if(subEditor->loadFile(filePath))
            {
                subEditor->show();
            }
            else
            {
                subEditor->close();
            }
        }
    }
}





































