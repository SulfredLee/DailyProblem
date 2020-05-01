#ifndef DEFAULTMUTEX_H
#define DEFAULTMUTEX_H
#include <pthread.h>

class DefaultMutex
{
 public:
    DefaultMutex();
    ~DefaultMutex();

    void Lock();
    void Unlock();
    pthread_mutex_t* GetMutex();
 private:
    pthread_mutexattr_t m_Attr;
    pthread_mutex_t m_Mutex;
};

class DefaultLock
{
 public:
    DefaultLock(DefaultMutex& defaultMutex);
    ~DefaultLock();
 private:
    DefaultMutex& m_defaultMutex;
};
#endif
