#include <QtGui/QApplication>

#include "hello.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    Hello hello;
    hello.show();
    return app.exec();
}
