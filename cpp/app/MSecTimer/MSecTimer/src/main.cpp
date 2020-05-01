#include <iostream>
#include <thread>
#include <chrono>

#include "MSecTimer.h"

class FooClass
{
public:
    FooClass() {}
    ~FooClass() {}

    static void PrintProxy(void *p, int x)
    {
        FooClass *c = (FooClass*)p;
        c->Print(x);
    }
    void Print(int x)
    {
        std::cout << "Print from class " << x << std::endl;
    }
};
void Foo(int x)
{
    std::cout << "Print from otuside " << x << std::endl;
}
void NormalCase()
{
    MSecTimer timer(1000, Foo, 10);
    timer.Start();
    int count = 0;
    while (count++ < 5)
    {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    timer.Stop();
}
void ClassCase()
{
    FooClass cc;
    MSecTimer timer(1000, FooClass::PrintProxy, &cc, 10);
    timer.Start();
    int count = 0;
    while (count++ < 5)
    {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    timer.Stop();
}
int main(int argc, char *argv[])
{
    NormalCase();
    ClassCase();

    return 0;
}
