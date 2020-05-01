#include <iostream>

#include "DefaultMutex.h"

// usage: ./DefaultMutexLinux
int main(int argc, char *argv[])
{
    {
        DefaultMutex defaultMutex;
        DefaultLock lock(defaultMutex);
        // Here is thread safe
    }
    return 0;
}
