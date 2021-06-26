#include "StdClassWithThread.h"
#include "Logger.h"

StdClassWithThread::StdClassWithThread()
{
    LOGMSG_CLASS_NAME("StdClassWithThread");
}

StdClassWithThread::~StdClassWithThread()
{
}

bool StdClassWithThread::InitComponent()
{
    StartThread();
    return true;
}

// override
void* StdClassWithThread::Main()
{
    LOGMSG_MSG("IN\n");

    while(IsThreadRunning())
    {
        if (!IsThreadRunning()) break;
    }

    LOGMSG_MSG("OUT\n");
    return NULL;
}
