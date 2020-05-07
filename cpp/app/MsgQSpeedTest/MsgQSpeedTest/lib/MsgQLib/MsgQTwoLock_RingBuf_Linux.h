#ifndef MSG_Q_TWOLOCK_RINGBUF_LINUX_H
#define MSG_Q_TWOLOCK_RINGBUF_LINUX_H
#include "DefaultMutex.h"
#include "MsgQBase.h"

#include <sys/time.h>

template<typename T>
class MsgQTwoLock_RingBuf_Linux : public MsgQBase<T>
{
 public:
    MsgQTwoLock_RingBuf_Linux()
    {
        m_inIndex = 0;
        m_outIndex = 0;
        m_ringBuf.resize(MAX_MSG_NUM);
        pthread_cond_init(&m_cond, NULL);
    }
    ~MsgQTwoLock_RingBuf_Linux()
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
    int GetInIndex();
 private:
    DefaultMutex m_outMutex;
    DefaultMutex m_inMutex;
    pthread_cond_t m_cond;
    int m_inIndex;
    int m_outIndex;
    std::vector<std::shared_ptr<T> > m_ringBuf;
};

// override MsgQBase<T>
template<typename T>
bool MsgQTwoLock_RingBuf_Linux<T>::AddMsg(std::shared_ptr<T>& msg)
{
    {
        DefaultLock lock(m_inMutex);
        int nextInIndex = ((m_inIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
        if (nextInIndex == m_outIndex) // if the next index of IN is index of OUT, that means buffer is full
        {
            pthread_cond_signal(&m_cond);
            nextInIndex = ((m_inIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
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
bool MsgQTwoLock_RingBuf_Linux<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    {
        DefaultLock lock(m_inMutex);
        int nextInIndex = ((m_inIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
        if (nextInIndex == m_outIndex) // if the next index of IN is index of OUT, that means buffer is full
        {
            pthread_cond_signal(&m_cond);
            nextInIndex = ((m_inIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
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
void MsgQTwoLock_RingBuf_Linux<T>::GetMsg(std::shared_ptr<T>& msg)
{
    pthread_mutex_lock(m_outMutex.GetMutex());
    while (m_outIndex == GetInIndex()) // if no more data in queue
    {
        pthread_cond_wait(&m_cond, m_outMutex.GetMutex());
    }
    msg = m_ringBuf[m_outIndex];
    int nextOutIndex = ((m_outIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
    m_outIndex = nextOutIndex;
    pthread_mutex_unlock(m_outMutex.GetMutex());
}
// override MsgQBase<T>
template<typename T>
int MsgQTwoLock_RingBuf_Linux<T>::GetMsgNum()
{
    DefaultLock lock2(m_outMutex);
    DefaultLock lock(m_inMutex);

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
void MsgQTwoLock_RingBuf_Linux<T>::Flush()
{
    DefaultLock lock2(m_outMutex);
    DefaultLock lock(m_inMutex);
    m_inIndex = m_outIndex;
}
// override MsgQBase<T>
template<typename T>
std::string MsgQTwoLock_RingBuf_Linux<T>::GetQName()
{
    return "MsgQTwoLock_RingBuf_Linux";
}
template<typename T>
int MsgQTwoLock_RingBuf_Linux<T>::GetInIndex()
{
    DefaultLock lock(m_inMutex);
    return m_inIndex;
}
#endif
