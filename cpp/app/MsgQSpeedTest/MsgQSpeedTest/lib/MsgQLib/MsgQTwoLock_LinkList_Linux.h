#ifndef MSG_Q_TWOLOCK_LINKLIST_LINUX_H
#define MSG_Q_TWOLOCK_LINKLIST_LINUX_H
#include "DefaultMutex.h"
#include "MsgQBase.h"
#include "Logger.h"

#include <atomic>
#include <thread>

template<typename T>
class MsgQTwoLock_LinkList_Linux : public MsgQBase<T>
{
 private:
    struct node
    {
        std::shared_ptr<T> data;
        std::unique_ptr<node> next;
    };
 public:
    MsgQTwoLock_LinkList_Linux()
        : m_head(new node)
        , m_tail(m_head.get())
    {
        LOGMSG_CLASS_NAME("MsgQTwoLock_LinkList_Linux");
        m_totalMsg = 0;
        pthread_cond_init(&m_cond, NULL);
    }
    ~MsgQTwoLock_LinkList_Linux()
    {
        pthread_cond_destroy(&m_cond);
    }
    MsgQTwoLock_LinkList_Linux (const MsgQTwoLock_LinkList_Linux& other) = delete;
    MsgQTwoLock_LinkList_Linux& operator= (const MsgQTwoLock_LinkList_Linux& other) = delete;

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
        DefaultLock lock(m_tailMutex);
        return m_tail;
    }
    std::unique_ptr<node> PopHead()
    {
        while (m_head.get() == GetTail())
        {
            pthread_cond_wait(&m_cond, m_headMutex.GetMutex());
        }
        std::unique_ptr<node> oldHead = std::move(m_head);
        m_head = std::move(oldHead->next);
        m_totalMsg--;
        return oldHead;
    }
 private:
    DefaultMutex m_headMutex;
    std::unique_ptr<node> m_head;
    DefaultMutex m_tailMutex;
    node *m_tail;
    pthread_cond_t m_cond;
    std::atomic<int> m_totalMsg;
};

// override MsgQBase<T>
template<typename T>
bool MsgQTwoLock_LinkList_Linux<T>::AddMsg(std::shared_ptr<T>& msg)
{
    std::unique_ptr<node> p(new node);
    node * const newTail = p.get();
    {
        DefaultLock lock(m_tailMutex);
        m_tail->data = std::move(msg);
        m_tail->next = std::move(p);
        m_tail = newTail;
        m_totalMsg++;
    }
    pthread_cond_signal(&m_cond);

    return true;
}

// override MsgQBase<T>
template<typename T>
bool MsgQTwoLock_LinkList_Linux<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    std::unique_ptr<node> p(new node);
    node * const newTail = p.get();
    {
        DefaultLock lock(m_tailMutex);
        m_tail->data = std::move(msg);
        m_tail->next = std::move(p);
        m_tail = newTail;
        m_totalMsg++;
    }
    pthread_cond_signal(&m_cond);

    return true;
}

// override MsgQBase<T>
template<typename T>
void MsgQTwoLock_LinkList_Linux<T>::GetMsg(std::shared_ptr<T>& msg)
{
    DefaultLock lock(m_headMutex);
    std::unique_ptr<node> oldHead = PopHead();
    msg = oldHead ? oldHead->data : std::shared_ptr<T>();
}

// override MsgQBase<T>
template<typename T>
int MsgQTwoLock_LinkList_Linux<T>::GetMsgNum()
{
    return m_totalMsg;
}

// override MsgQBase<T>
template<typename T>
void MsgQTwoLock_LinkList_Linux<T>::Flush()
{
}

// override MsgQBase<T>
template<typename T>
std::string MsgQTwoLock_LinkList_Linux<T>::GetQName()
{
    return "MsgQTwoLock_LinkList_Linux";
}
#endif
