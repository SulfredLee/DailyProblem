#include <stdlib.h>
#include <pthread.h>
// private
typedef struct MsgQ_C
{
    void** pData; // this is an array and we use it as a ring buffer
    int length;
    int inIndex;
    int outIndex;
    pthread_mutex_t headMutex;
    pthread_mutex_t tailMutex;
    pthread_cond_t cond;
}MsgQ_C;

// public
MsgQ_C* createMsgQ_C()
{
    MsgQ_C* pQueue = (MsgQ_C*)malloc(sizeof(MsgQ_C));
    pQueue->pData = malloc(sizeof(void*) * 128);
    pQueue->length = 128;

    pthread_mutexattr_t attr;
    pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_DEFAULT);
    pthread_mutex_init(&(pQueue->headMutex), &attr);
    pthread_mutex_init(&(pQueue->tailMutex), &attr);
    pthread_cond_init(&(pQueue->cond), NULL);
    return pQueue;
}

void freeMsgQ_C(MsgQ_C* inQueue)
{
    free(inQueue->pData);
    pthread_mutex_destroy(&(inQueue->headMutex));
    pthread_mutex_destroy(&(inQueue->tailMutex));
    pthread_cond_destroy(&(inQueue->cond));
    inQueue = NULL;
}

int pushMsgQ_C(void** inData, MsgQ_C* inQueue)
{
    if (inQueue == NULL || inData == NULL)
    {
        return 0;
    }
    pthread_mutex_lock(&(inQueue->headMutex));
    int nextInIndex = ((inQueue->inIndex + 1) & (128 - 1)); // mod operation
    if (nextInIndex == inQueue->outIndex){ // if the next index of IN is index of OUT
        pthread_mutex_unlock(&(inQueue->headMutex));
        return 0;
    }
    inQueue->pData[inQueue->inIndex] = *inData;
    __sync_val_compare_and_swap(&(inQueue->inIndex), inQueue->inIndex, nextInIndex); // InterlockedCompareExchange((long*)&m_nIN, nNextIN, m_nIN);
    pthread_mutex_unlock(&(inQueue->headMutex));
    pthread_cond_signal(&(inQueue->cond));
    return 1; // success
}

int getMsgQ_C(void ** outData, MsgQ_C* inQueue)
{
    if (inQueue == NULL)
    {
        return 0;
    }
    pthread_mutex_lock(&(inQueue->tailMutex));
    while (inQueue->outIndex == inQueue->inIndex){ // if no more data in queue
        pthread_cond_wait(&(inQueue->cond), &(inQueue->tailMutex));
        //return false;
    }
    *outData = inQueue->pData[inQueue->outIndex];
    int nextOutIndex = ((inQueue->outIndex + 1) & (128 - 1)); // mod operation
    __sync_val_compare_and_swap(&(inQueue->outIndex), inQueue->outIndex, nextOutIndex); // InterlockedCompareExchange((long*)&m_nOUT, nNextOUT, m_nOUT);
    pthread_mutex_unlock(&(inQueue->tailMutex));
    return 1;
}
