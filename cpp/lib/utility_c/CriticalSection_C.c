#include <stdlib.h>
#include <string.h>
#include <pthread.h>

// private
typedef struct CriticalSection_C
{
    pthread_mutexattr_t m_Attr;
    pthread_mutex_t m_Mutex;
}CriticalSection_C;

// public
CriticalSection_C* createCriticalSection_C()
{
    CriticalSection_C* pMutex = (CriticalSection_C*)malloc(sizeof(CriticalSection_C));
    memset(pMutex, 0, sizeof(CriticalSection_C));

    pthread_mutexattr_settype(&(pMutex->m_Attr), PTHREAD_MUTEX_RECURSIVE);
    pthread_mutex_init(&(pMutex->m_Mutex), &(pMutex->m_Attr));

    return pMutex;
}

void freeCriticalSection_C(struct CriticalSection_C** inMutex)
{
    if (*inMutex)
    {
        pthread_mutex_destroy(&((*inMutex)->m_Mutex));
        free(*inMutex);
        *inMutex = NULL;
    }
}

void Lock_CriticalSection_C(struct CriticalSection_C* inMutex)
{
    pthread_mutex_lock(&(inMutex->m_Mutex));
}

void Unlocak_CriticalSection_C(struct CriticalSection_C* inMutex)
{
    pthread_mutex_unlock(&(inMutex->m_Mutex));
}
