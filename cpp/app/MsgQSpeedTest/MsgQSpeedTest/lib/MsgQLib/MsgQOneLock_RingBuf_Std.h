#ifndef MSG_Q_ONELOCK_RINGBUF_STD_H
#define MSG_Q_ONELOCK_RINGBUF_STD_H
#include "MsgQBase.h"

#include <sys/time.h>
#include <atomic>
#include <thread>
#include <mutex>
#include <condition_variable>

template<typename T>
class MsgQOneLock_RingBuf_Std : public MsgQBase<T>
{
 public:
    MsgQOneLock_RingBuf_Std()
    {
        m_inIndex = 0;
        m_outIndex = 0;
        m_ringBuf.resize(MAX_MSG_NUM);
    }
    ~MsgQOneLock_RingBuf_Std()
    {
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
    std::mutex m_mutex;
    std::condition_variable m_cond;
    int m_inIndex;
    int m_outIndex;
    std::vector<std::shared_ptr<T> > m_ringBuf;
};

// override MsgQBase<T>
template<typename T>
bool MsgQOneLock_RingBuf_Std<T>::AddMsg(std::shared_ptr<T>& msg)
{
    {
        std::lock_guard<std::mutex> lock(m_mutex);
        int nextInIndex = ((m_inIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
        if (nextInIndex == m_outIndex) // if the next index of IN is index of OUT, that means buffer is full
        {
            m_cond.notify_one();
            return false;
        }

        m_ringBuf[m_inIndex] = std::move(msg);
        m_inIndex = nextInIndex;
    }
    m_cond.notify_one();
    return true;
}
// override MsgQBase<T>
template<typename T>
bool MsgQOneLock_RingBuf_Std<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    {
        std::lock_guard<std::mutex> lock(m_mutex);
        int nextInIndex = ((m_inIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
        if (nextInIndex == m_outIndex) // if the next index of IN is index of OUT, that means buffer is full
        {
            m_cond.notify_one();
            return false;
        }

        m_ringBuf[m_inIndex] = std::move(msg);
        m_inIndex = nextInIndex;
    }
    m_cond.notify_one();
    return true;
}
// override MsgQBase<T>
template<typename T>
void MsgQOneLock_RingBuf_Std<T>::GetMsg(std::shared_ptr<T>& msg)
{
    std::unique_lock<std::mutex> lock(m_mutex);
    m_cond.wait(lock, [&] { return m_outIndex != m_inIndex; });

    msg = m_ringBuf[m_outIndex];
    int nextOutIndex = ((m_outIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
    m_outIndex = nextOutIndex;
}
// override MsgQBase<T>
template<typename T>
int MsgQOneLock_RingBuf_Std<T>::GetMsgNum()
{
    std::lock_guard<std::mutex> lock(m_mutex);

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
void MsgQOneLock_RingBuf_Std<T>::Flush()
{
    std::lock_guard<std::mutex> lock(m_mutex);
    m_inIndex = m_outIndex;
}
// override MsgQBase<T>
template<typename T>
std::string MsgQOneLock_RingBuf_Std<T>::GetQName()
{
    return "MsgQOneLock_RingBuf_Std";
}
#endif
