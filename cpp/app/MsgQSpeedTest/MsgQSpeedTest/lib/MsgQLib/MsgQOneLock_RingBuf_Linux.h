#ifndef MSG_Q_ONELOCK_RINGBUF_LINUX_H
#define MSG_Q_ONELOCK_RINGBUF_LINUX_H
#include "DefaultMutex.h"
#include "MsgQBase.h"

#include <sys/time.h>

template<typename T>
class MsgQOneLock_RingBuf_Linux : public MsgQBase<T>
{
 public:
    MsgQOneLock_RingBuf_Linux()
    {
        m_inIndex = 0;
        m_outIndex = 0;
        m_ringBuf.resize(MAX_MSG_NUM);
        pthread_cond_init(&m_cond, NULL);
    }
    ~MsgQOneLock_RingBuf_Linux()
    {
        pthread_cond_destroy(&m_cond);
    }

    // override MsgQBase<T>
    bool AddMsg(std::shared_ptr<T>& msg);
    // override MsgQBase<T>
    bool AddMsg(std::shared_ptr<T>&& msg);
    // override MsgQBase<T>
    void GetMsg(std::shared_ptr<T>& msg);
    // override MsgQBase<T>
    int GetMsgNum();
    // override MsgQBase<T>
    void Flush();
    // override MsgQBase<T>
    std::string GetQName();
 private:
    DefaultMutex m_mutex;
    pthread_cond_t m_cond;
    int m_inIndex;
    int m_outIndex;
    std::vector<std::shared_ptr<T> > m_ringBuf;
};

// override MsgQBase<T>
template<typename T>
bool MsgQOneLock_RingBuf_Linux<T>::AddMsg(std::shared_ptr<T>& msg)
{
    {
        DefaultLock lock(m_mutex);
        int nextInIndex = ((m_inIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
        if (nextInIndex == m_outIndex) // if the next index of IN is index of OUT, that means buffer is full
        {
            pthread_cond_signal(&m_cond);
            return false;
        }

        m_ringBuf[m_inIndex] = std::move(msg);
        m_inIndex = nextInIndex;
    }
    pthread_cond_signal(&m_cond);
    return true;
}
// override MsgQBase<T>
template<typename T>
bool MsgQOneLock_RingBuf_Linux<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    {
        DefaultLock lock(m_mutex);
        int nextInIndex = ((m_inIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
        if (nextInIndex == m_outIndex) // if the next index of IN is index of OUT, that means buffer is full
        {
            pthread_cond_signal(&m_cond);
            return 0;
        }

        m_ringBuf[m_inIndex] = std::move(msg);
        m_inIndex = nextInIndex;
    }
    pthread_cond_signal(&m_cond);
    return true;
}
// override MsgQBase<T>
template<typename T>
void MsgQOneLock_RingBuf_Linux<T>::GetMsg(std::shared_ptr<T>& msg)
{
    pthread_mutex_lock(m_mutex.GetMutex());
    while (m_outIndex == m_inIndex) // if no more data in queue
    {
        pthread_cond_wait(&m_cond, m_mutex.GetMutex());
    }
    msg = m_ringBuf[m_outIndex];
    int nextOutIndex = ((m_outIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
    m_outIndex = nextOutIndex;
    pthread_mutex_unlock(m_mutex.GetMutex());
}
// override MsgQBase<T>
template<typename T>
int MsgQOneLock_RingBuf_Linux<T>::GetMsgNum()
{
    DefaultLock lock(m_mutex);

    int inIndex = m_inIndex;
    int outIndex = m_outIndex;

    if (inIndex > outIndex)
        return inIndex - outIndex;
    else if (outIndex > inIndex)
        return MAX_MSG_NUM - outIndex + inIndex;
    else
        return 0;
}
// override MsgQBase<T>
template<typename T>
void MsgQOneLock_RingBuf_Linux<T>::Flush()
{
    DefaultLock lock(m_mutex);
    m_inIndex = m_outIndex;
}
// override MsgQBase<T>
template<typename T>
std::string MsgQOneLock_RingBuf_Linux<T>::GetQName()
{
    return "MsgQOneLock_RingBuf_Linux";
}
#endif
