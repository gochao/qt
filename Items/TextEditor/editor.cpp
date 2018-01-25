#include "editor.h"
#include <QFile>
#include <QMessageBox>
#include <QTextStream>
#include <QApplication>
#include <QFileInfo>
#include <QFileDialog>
#include <QCloseEvent>

Editor::Editor(QWidget *parent)
{
    setAttribute(Qt::WA_DeleteOnClose);
    isUntitled = true;
}


void Editor::newFile()
{
    //设置窗口编号，一直叠加因此设置为静态变量
    static int sequenceNumber = 1;

    isUntitled = true;

    curFile = tr("未命名文档%1.txt").arg(sequenceNumber++);
    
    //标题 “[*]”由函数决定是否添加
    setWindowTitle(curFile + "[*]");

    //文档被修改后信号触发自定的槽函数，设置文档标题
    connect(document(), &QTextDocument::contentsChanged, this, &Editor::documentWasModified);
}


void Editor::documentWasModified()
{
    //根据文档修改状态设置，在窗口标题加“*”
    setWindowModified(document()->isModified());
}

bool Editor::loadFile(const QString &filePath)
{
    QFile file(filePath);

    if(!file.open(QFile::ReadOnly | QFile::Text))
    {
        QMessageBox::warning(
            this,
            tr("多文档编辑器"),
            tr("无法读取文件%1\n%2").arg(filePath).arg(file.errorString())
            );
        return false;
    }

    //读取流
    QTextStream in(&file);

    //修改光标
    QApplication::setOverrideCursor(Qt::WaitCursor);
    //将读取的内容按纯文本格式输入到Editor中
    setPlainText(in.readAll());
    //恢复光标
    QApplication::restoreOverrideCursor();

    //设置当前文档名
    setCurrentFile(filePath);

    //将文档的修改状态链接到槽
    connect(document(), &QTextDocument::contentsChanged, this, &Editor::documentWasModified);

    return true;
}


void Editor::setCurrentFile(const QString &filePath)
{
    curFile = QFileInfo(filePath).canonicalFilePath();
    
    isUntitled = false;

    document()->setModified(false);
    setWindowModified(false);
    setWindowTitle(userFriendlyCurrentFile() + "[*]");
}


QString Editor::userFriendlyCurrentFile()
{
    return QFileInfo(curFile).fileName();
}


bool Editor::save()
{
    if(isUntitled)
    {
        return saveAs();
    }
    else
    {
        return saveFile(curFile);
    }
}

bool Editor::saveAs()
{
    QString filePath = QFileDialog::getSaveFileName(this, tr("另存为"), curFile, tr("文本文件(*.txt)"));

    if(filePath.isEmpty())
    {
        return false;
    }
    else
    {
        return saveFile(filePath);
    }
}

bool Editor::saveFile(const QString &filePath)
{
    QFile file(filePath);
    if(!file.open(QFile::WriteOnly|QFile::Text))
    {
        QMessageBox::warning(
            this,tr("多文档编辑器"),
            tr("无法写入文件")
            );

        return false;
    }

    //输出流
    QTextStream out(&file);

    QApplication::setOverrideCursor(Qt::WaitCursor);
    out << toPlainText();
    QApplication::restoreOverrideCursor();
    
    //重修修改当前文件名
    setCurrentFile(filePath);
    
    return true;
}

void Editor::closeEvent(QCloseEvent *event)
{
    //如果需要存储，则将关闭事件在此处accept，不让其传播
    if(maybeSave())
    {
        event->accept();
    }
    else
    {
        QTextEdit::closeEvent(event);
    }
}


bool Editor::maybeSave()
{
    if(document()->isModified())
    {
        if(QMessageBox::Yes == QMessageBox::question(
            this,
            tr("未保存文件"),
            tr("是否保存对 %1 的更改?").arg(userFriendlyCurrentFile()),
            QMessageBox::Yes |QMessageBox::No,
            QMessageBox::Yes
            )
            )
        {
            return save();
        }
        else
        {
            return false;
        }
    }

    return true;
}







































