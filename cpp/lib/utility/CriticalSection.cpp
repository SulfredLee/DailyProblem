#include "CriticalSection.h"

CriticalSection::CriticalSection()
{
    pthread_mutexattr_init(&m_Attr);
    pthread_mutexattr_settype(&m_Attr, PTHREAD_MUTEX_RECURSIVE);
    pthread_mutex_init(&m_Mutex, &m_Attr);
}

CriticalSection::~CriticalSection()
{
    pthread_mutex_destroy(&m_Mutex);
}

void CriticalSection::Lock()
{
    pthread_mutex_lock(&m_Mutex);
}

void CriticalSection::Unlock()
{
    pthread_mutex_unlock(&m_Mutex);
}

CriticalLock::CriticalLock(CriticalSection& section) : m_section(section)
{
    m_section.Lock();
}

CriticalLock::~CriticalLock()
{
    m_section.Unlock();
}
