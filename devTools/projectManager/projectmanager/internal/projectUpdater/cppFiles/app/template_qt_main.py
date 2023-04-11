content_st = """
#include <iostream>

#include <QApplication>
#include "mainwindow.h"

int main (int argc, char *argv[])
{
    QApplication app(argc, argv);

    MainWindow MW;
    MW.show();
    bool bRTN = app.exec();

    return bRTN;
}
"""
