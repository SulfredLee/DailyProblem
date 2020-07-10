// run as sudo ./PingRemake <hostname>

#include <iostream>
#include "ping.h"
Ping pinger;

// Interrupt handler
void intHandler(int dummy)
{
    pinger.intHandler();
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        std::cout << "Format " << argv[0] << " <address>" << std::endl;
        return 0;
    }

    signal(SIGINT, intHandler);//catching interrupt

    pinger.SendPing(argv[1]);


    return 0;
}
