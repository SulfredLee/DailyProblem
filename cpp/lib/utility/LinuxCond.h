#ifndef LINUX_COND_H
#define LINUX_COND_H
#include <pthread.h>

#include "DefaultMutex.h"

class LinuxCond
{
 public:
    LinuxCond();
    ~LinuxCond();

    void Signal();
    int WaitWithTime(int MSec);
    int Wait();
 private:
    pthread_cond_t m_cond;
    DefaultMutex m_mutex;
};

#endif
