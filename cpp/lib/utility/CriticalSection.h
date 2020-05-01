#ifndef CRITICALSECTION_H
#define CRITICALSECTION_H
#include <pthread.h>

class CriticalSection
{
 public:
    CriticalSection();
    ~CriticalSection();

    void Lock();
    void Unlock();
 private:
    pthread_mutexattr_t m_Attr;
    pthread_mutex_t m_Mutex;
};

class CriticalLock
{
 public:
    CriticalLock(CriticalSection& section);
    ~CriticalLock();
 private:
    CriticalSection& m_section;
};
#endif
