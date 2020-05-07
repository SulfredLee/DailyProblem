#ifndef MSG_Q_LOCKFREE_COMPLETE_LINKLIST_STD_H
#define MSG_Q_LOCKFREE_COMPLETE_LINKLIST_STD_H
#include "MsgQBase.h"
#include "Logger.h"

#include <atomic>
#include <thread>
#include <mutex>
#include <condition_variable>

template<typename T>
class MsgQLockFree_Complete_LinkList_Std : public MsgQBase<T>
{
 private:
    struct node;
    struct countedNodePtr;
 public:
    MsgQLockFree_Complete_LinkList_Std()
    {
        LOGMSG_CLASS_NAME("MsgQLockFree_Complete_LinkList_Std");
    }
    ~MsgQLockFree_Complete_LinkList_Std()
    {
    }
    MsgQLockFree_Complete_LinkList_Std (const MsgQLockFree_Complete_LinkList_Std& other) = delete;
    MsgQLockFree_Complete_LinkList_Std& operator= (const MsgQLockFree_Complete_LinkList_Std& other) = delete;

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
    static void increaseExternalCount(std::atomic<countedNodePtr>& counter, countedNodePtr& oldCounter)
    {
        countedNodePtr newCounter;

        do
        {
            newCounter = oldCounter;
            ++newCounter.m_externalCount;
        }
        while (!counter.compare_exchange_strong(oldCounter, newCounter, std::memory_order_acquire, std::memory_order_relaxed));

        oldCounter.m_externalCount = newCounter.m_externalCount;
    }
    static void freeExternalCounter(countedNodePtr &oldNodePtr)
    {
        node * const ptr = oldNodePtr.m_ptr;
        int const countIncrease = oldNodePtr.m_externalCount - 2;

        nodeCounter oldCounter = ptr->m_count.load(std::memory_order_relaxed);
        nodeCounter newCounter;
        do
        {
            newCounter = oldCounter;
            --newCounter.m_externalCounters;
            newCounter.m_internalCount += countIncrease;
        }
        while (!ptr->m_count.compare_exchange_strong(oldCounter, newCounter, std::memory_order_acquire, std::memory_order_relaxed));

        if (!newCounter.m_internalCount && !newCounter.m_externalCounters)
        {
            delete ptr;
        }
    }
 private:
    struct countedNodePtr
    {
        int m_externalCount;
        node *m_ptr;
    };
    struct nodeCounter
    {
        unsigned m_internalCount:30;
        unsigned m_externalCounters:2;
    };
    struct node
    {
        std::atomic<T*> m_data;
        std::atomic<nodeCounter> m_count;
        countedNodePtr m_next;

        node ()
        {
            nodeCounter newCount;
            newCount.m_internalCount = 0;
            newCount.m_externalCounters = 2;
            m_count.store(newCount);

            m_next.m_ptr = nullptr;
            m_next.m_externalCount = 0;
        }
        void releaseRef()
        {
            nodeCounter oldCounter = m_count.load(std::memory_order_relaxed);
            nodeCounter newCounter;
            do
            {
                newCounter = oldCounter;
                --newCounter.m_internalCount;
            }
            while (!m_count.compare_exchange_strong(oldCounter, newCounter, std::memory_order_acquire, std::memory_order_relaxed));

            if (!newCounter.m_internalCount && !newCounter.m_externalCounters)
            {
                delete this;
            }
        }
    };
    std::atomic<countedNodePtr> m_head;
    std::atomic<countedNodePtr> m_tail;
};

// override MsgQBase<T>
template<typename T>
bool MsgQLockFree_Complete_LinkList_Std<T>::AddMsg(std::shared_ptr<T>& msg)
{
    std::unique_ptr<T> newData(new T(*msg));
    countedNodePtr newNext;
    newNext.m_ptr = new node;
    newNext.m_externalCount = 1;
    countedNodePtr oldTail = m_tail.load();

    for (;;)
    {
        increaseExternalCount(m_tail, oldTail);

        T *oldData = nullptr;
        if (oldTail.m_ptr->m_data.compare_exchange_strong(oldData, newData.get()))
        {
            oldTail.m_ptr->m_next = newNext;
            oldTail = m_tail.exchange(newNext);
            freeExternalCounter(oldTail);
            newData.release();
            break;
        }
        oldTail.m_ptr->releaseRef();
    }

    return true;
}
// override MsgQBase<T>
template<typename T>
bool MsgQLockFree_Complete_LinkList_Std<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    std::unique_ptr<T> newData(new T(*msg));
    countedNodePtr newNext;
    newNext.m_ptr = new node;
    newNext.m_externalCount = 1;
    countedNodePtr oldTail = m_tail.load();

    for (;;)
    {
        increaseExternalCount(m_tail, oldTail);

        T *oldData = nullptr;
        if (oldTail.m_ptr->m_data.compare_exchange_strong(oldData, newData.get()))
        {
            oldTail.m_ptr->m_next = newNext;
            oldTail = m_tail.exchange(newNext);
            freeExternalCounter(oldTail);
            newData.release();
            break;
        }
        oldTail.m_ptr->releaseRef();
    }

    return true;
}
// override MsgQBase<T>
template<typename T>
void MsgQLockFree_Complete_LinkList_Std<T>::GetMsg(std::shared_ptr<T>& msg)
{
    countedNodePtr oldHead = m_head.load(std::memory_order_relaxed);
    for (;;)
    {
        increaseExternalCount(m_head, oldHead);
        node * const ptr = oldHead.m_ptr;
        if (ptr == m_tail.load().m_ptr)
        {
            ptr->releaseRef();
            msg = std::shared_ptr<T>();
        }
        if (m_head.compare_exchange_strong(oldHead, ptr->m_next))
        {
            T* const res = ptr->m_data.exchange(nullptr);
            freeExternalCounter(oldHead);
            msg = std::shared_ptr<T>(res);
        }
        ptr->releaseRef();
    }
}
// override MsgQBase<T>
template<typename T>
int MsgQLockFree_Complete_LinkList_Std<T>::GetMsgNum()
{
    return 0;
}
// override MsgQBase<T>
template<typename T>
void MsgQLockFree_Complete_LinkList_Std<T>::Flush()
{
}
// override MsgQBase<T>
template<typename T>
std::string MsgQLockFree_Complete_LinkList_Std<T>::GetQName()
{
    return "MsgQLockFree_Complete_LinkList_Std";
}

#endif
