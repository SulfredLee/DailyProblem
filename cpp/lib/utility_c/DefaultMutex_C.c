#include <stdlib.h>
#include <string.h>
#include <pthread.h>

// private
typedef struct DefaultMutex_C
{
    pthread_mutexattr_t m_Attr;
    pthread_mutex_t m_Mutex;
}DefaultMutex_C;

// public
DefaultMutex_C* createDefaultMutex_C()
{
    DefaultMutex_C* pMutex = (DefaultMutex_C*)malloc(sizeof(DefaultMutex_C));
    memset(pMutex, 0, sizeof(DefaultMutex_C));

    pthread_mutexattr_init(&(pMutex->m_Attr));
    pthread_mutexattr_settype(&(pMutex->m_Attr), PTHREAD_MUTEX_DEFAULT);
    pthread_mutex_init(&(pMutex->m_Mutex), &(pMutex->m_Attr));

    return pMutex;
}

void freeDefaultMutex_C(struct DefaultMutex_C** inMutex)
{
    if (*inMutex)
    {
        pthread_mutex_destroy(&((*inMutex)->m_Mutex));
        free(*inMutex);
        *inMutex = NULL;
    }
}

void Lock_DefaultMutex_C(struct DefaultMutex_C* inMutex)
{
    pthread_mutex_lock(&(inMutex->m_Mutex));
}

void Unlocak_DefaultMutex_C(struct DefaultMutex_C* inMutex)
{
    pthread_mutex_unlock(&(inMutex->m_Mutex));
}
