#include "DefaultMutex.h"

DefaultMutex::DefaultMutex()
{
    pthread_mutexattr_init(&m_Attr);
    pthread_mutexattr_settype(&m_Attr, PTHREAD_MUTEX_DEFAULT);
    pthread_mutex_init(&m_Mutex, &m_Attr);
}

DefaultMutex::~DefaultMutex()
{
    pthread_mutex_destroy(&m_Mutex);
}

void DefaultMutex::Lock()
{
    pthread_mutex_lock(&m_Mutex);
}

void DefaultMutex::Unlock()
{
    pthread_mutex_unlock(&m_Mutex);
}

pthread_mutex_t* DefaultMutex::GetMutex()
{
    return &m_Mutex;
}

DefaultLock::DefaultLock(DefaultMutex& defaultMutex) : m_defaultMutex(defaultMutex)
{
    m_defaultMutex.Lock();
}

DefaultLock::~DefaultLock()
{
    m_defaultMutex.Unlock();
}
