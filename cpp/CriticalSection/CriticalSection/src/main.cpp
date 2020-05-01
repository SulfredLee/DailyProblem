#include <iostream>
#include "CriticalSection.h"

CriticalSection section;

void FooLoop(int thisCount)
{
    CriticalLock lock(section);
    if (thisCount < 10)
    {
        std::cout << "count: " << thisCount++ << std::endl;
        FooLoop(thisCount);
    }
    else
        return;
}

int main(int argc, char *argv[])
{
    FooLoop(0);

    return 0;
}
