#ifndef MSG_Q_TWOLOCK_LINKLIST_STD_H
#define MSG_Q_TWOLOCK_LINKLIST_STD_H
#include "DefaultMutex.h"
#include "MsgQBase.h"
#include "Logger.h"

#include <atomic>
#include <thread>
#include <mutex>
#include <condition_variable>

template<typename T>
class MsgQTwoLock_LinkList_Std : public MsgQBase<T>
{
 private:
    struct node
    {
        std::shared_ptr<T> data;
        std::unique_ptr<node> next;
    };
 public:
    MsgQTwoLock_LinkList_Std()
        : m_head(new node)
        , m_tail(m_head.get())
    {
        LOGMSG_CLASS_NAME("MsgQTwoLock_LinkList_Std");
        m_totalMsg = 0;
    }
    ~MsgQTwoLock_LinkList_Std()
    {
    }
    MsgQTwoLock_LinkList_Std (const MsgQTwoLock_LinkList_Std& other) = delete;
    MsgQTwoLock_LinkList_Std& operator= (const MsgQTwoLock_LinkList_Std& other) = delete;

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
    node *GetTail()
    {
        std::lock_guard<std::mutex> lock(m_tailMutex);
        return m_tail;
    }
    std::unique_lock<std::mutex> WaitForData()
    {
        std::unique_lock<std::mutex> lock(m_headMutex);
        m_cond.wait(lock, [&] { return m_head.get() != GetTail(); });
        return lock;
    }
    std::unique_ptr<node> PopHead()
    {
        std::unique_ptr<node> oldHead = std::move(m_head);
        m_head = std::move(oldHead->next);
        m_totalMsg--;
        return oldHead;
    }
 private:
    std::mutex m_headMutex;
    std::unique_ptr<node> m_head;
    std::mutex m_tailMutex;
    node *m_tail;
    std::condition_variable m_cond;
    std::atomic<int> m_totalMsg;
};

// override MsgQBase<T>
template<typename T>
bool MsgQTwoLock_LinkList_Std<T>::AddMsg(std::shared_ptr<T>& msg)
{
    std::unique_ptr<node> p(new node);
    node * const newTail = p.get();
    {
        std::lock_guard<std::mutex> lock(m_tailMutex);
        m_tail->data = std::move(msg);
        m_tail->next = std::move(p);
        m_tail = newTail;
        m_totalMsg++;
    }
    m_cond.notify_one();

    return true;
}

// override MsgQBase<T>
template<typename T>
bool MsgQTwoLock_LinkList_Std<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    std::unique_ptr<node> p(new node);
    node * const newTail = p.get();
    {
        std::lock_guard<std::mutex> lock(m_tailMutex);
        m_tail->data = std::move(msg);
        m_tail->next = std::move(p);
        m_tail = newTail;
        m_totalMsg++;
    }
    m_cond.notify_one();

    return true;
}

// override MsgQBase<T>
template<typename T>
void MsgQTwoLock_LinkList_Std<T>::GetMsg(std::shared_ptr<T>& msg)
{
    std::unique_lock<std::mutex> lock(WaitForData());
    std::unique_ptr<node> oldHead = PopHead();
    msg = oldHead ? oldHead->data : std::shared_ptr<T>();
}

// override MsgQBase<T>
template<typename T>
int MsgQTwoLock_LinkList_Std<T>::GetMsgNum()
{
    return m_totalMsg;
}

// override MsgQBase<T>
template<typename T>
void MsgQTwoLock_LinkList_Std<T>::Flush()
{
}

// override MsgQBase<T>
template<typename T>
std::string MsgQTwoLock_LinkList_Std<T>::GetQName()
{
    return "MsgQTwoLock_LinkList_Std";
}
#endif
