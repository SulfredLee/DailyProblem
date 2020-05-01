#ifndef LINUX_THREAD_H
#define LINUX_THREAD_H
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "SafeData.h"

class LinuxThread
{
 public:
    LinuxThread();
    virtual ~LinuxThread();
 protected:
    virtual void* Main() = 0;

    bool startThread();
    void stopThread();
    void joinThread();
    bool isThreadRunning();
 private:
    static void* MainProxy(void* context);

 protected:
    pthread_t m_thread;
 private:
    SafeData<bool> m_run;
};

#endif
