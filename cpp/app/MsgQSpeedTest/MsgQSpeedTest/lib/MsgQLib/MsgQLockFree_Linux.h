//--------------------------------------------- Readme
// This structure only support single-producer and signle-consumer
//--------------------------------------------- Readme

#ifndef MSG_Q_LOCK_FREE_LINUX_H
#define MSG_Q_LOCK_FREE_LINUX_H
#include <vector>

#include "MsgQBase.h"
#include "LinuxCond.h"

#define FASTER 1

template<typename T>
class MsgQLockFree_Linux : public MsgQBase<T>
{
 public:
    MsgQLockFree_Linux()
    {
        m_inIndex = 0;
        m_outIndex = 0;
        m_ringBuf.resize(MAX_MSG_NUM);
    }
    ~MsgQLockFree_Linux()
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
    LinuxCond m_cond;
    int m_inIndex;
    int m_outIndex;
    std::vector<std::shared_ptr<T> > m_ringBuf;
};

// override MsgQBase<T>
template<typename T>
bool MsgQLockFree_Linux<T>::AddMsg(std::shared_ptr<T>& msg)
{
    int nextInIndex = ((m_inIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
    if (nextInIndex == m_outIndex) // if the next index of IN is index of OUT, that means buffer is full
    {
#ifndef FASTER
        m_cond.Signal();
#endif
        return 0;
    }

    m_ringBuf[m_inIndex] = std::move(msg);
    __sync_val_compare_and_swap(&m_inIndex, m_inIndex, nextInIndex); // InterlockedCompareExchange((long*)&m_nIN, nNextIN, m_nIN);
#ifndef FASTER
    m_cond.Signal();
#endif
    return true;
}

// override MsgQBase<T>
template<typename T>
bool MsgQLockFree_Linux<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    int nextInIndex = ((m_inIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
    if (nextInIndex == m_outIndex) // if the next index of IN is index of OUT, that means buffer is full
    {
#ifndef FASTER
        m_cond.Signal();
#endif
        return 0;
    }

    m_ringBuf[m_inIndex] = std::move(msg);
    __sync_val_compare_and_swap(&m_inIndex, m_inIndex, nextInIndex); // InterlockedCompareExchange((long*)&m_nIN, nNextIN, m_nIN);
#ifndef FASTER
    m_cond.Signal();
#endif
    return true;
}

// override MsgQBase<T>
template<typename T>
void MsgQLockFree_Linux<T>::GetMsg(std::shared_ptr<T>& msg)
{
    while (m_outIndex == m_inIndex) // if no more data in queue
    {
#ifndef FASTER
        m_cond.WaitWithTime(1);
#else
        __sync_val_compare_and_swap(&m_inIndex, m_inIndex, m_inIndex); // use this for higher speed
#endif
    }

    msg = m_ringBuf[m_outIndex];
    int nextOutIndex = ((m_outIndex + 1) & (MAX_MSG_NUM - 1)); // mod operation
    __sync_val_compare_and_swap(&m_outIndex, m_outIndex, nextOutIndex); // InterlockedCompareExchange((long*)&m_nOUT, nNextOUT, m_nOUT);
}

// override MsgQBase<T>
template<typename T>
int MsgQLockFree_Linux<T>::GetMsgNum()
{
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
void MsgQLockFree_Linux<T>::Flush()
{
}

// override MsgQBase<T>
template<typename T>
std::string MsgQLockFree_Linux<T>::GetQName()
{
    return "MsgQLockFree_Linux";
}

#endif
