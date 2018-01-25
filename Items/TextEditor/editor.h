#ifndef EDITOR_H
#define EDITOR_H

#include <QTextEdit>

class Editor : public QTextEdit
{
    Q_OBJECT

public:
    explicit Editor(QWidget *parent = 0);

    void newFile();
    bool loadFile(const QString &filePath);
    bool save();
    bool saveAs();
    bool saveFile(const QString &filePath);
    QString userFriendlyCurrentFile();
    QString currentFile(){return curFile;}

protected:
    void closeEvent(QCloseEvent * event);

private slots:
    void documentWasModified();

private:
    QString curFile;
    bool isUntitled;

    bool maybeSave();
    void setCurrentFile(const QString &filePath);
};

#endif // EDITOR_H
