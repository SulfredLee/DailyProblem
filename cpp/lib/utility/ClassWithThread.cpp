#include "ClassWithThread.h"
#include "Logger.h"

Trader::Trader()
{
    LOGMSG_CLASS_NAME("Trader");
}

Trader::~Trader()
{
    stopThread();
    joinThread();
}

bool Trader::InitComponent()
{
    startThread();
    return true;
}

// override
void* Trader::Main()
{
    LOGMSG_MSG("IN\n");

    while(isThreadRunning())
    {
        if (!isThreadRunning()) break;
    }

    LOGMSG_MSG("OUT\n");
    return NULL;
}
