#include <iostream>
#include <thread>
#include <string.h>
#include <unistd.h>

#include "MsgQ_C.h"
#include "Logger.h"

MsgQ_C* queue = createMsgQ_C();

void thread001Fun()
{
    int i = 0;
    while (true)
    {
        char* string = new char[1024];
        sprintf(string, "number %03d", i++);
        pushMsgQ_C((void**)&string, queue);
        usleep(500000); // sleep 0.5 sec
    }
}

void thread002Fun()
{
    int i = 1000;
    while (true)
    {
        char* string = new char[1024];
        sprintf(string, "number %03d", i++);
        pushMsgQ_C((void**)&string, queue);
        usleep(1000000); // sleep 1 sec
    }
}

int main(int argc, char* argv[])
{
    std::thread thread001(thread001Fun);
    std::thread thread002(thread002Fun);
    while (true)
    {
        char* string;
        getMsgQ_C((void**)&string, queue);
        LOGMSG_MSG_C("%s\n", string);
        delete string;
    }

    freeMsgQ_C(queue);
    return 0;
}
