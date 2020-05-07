//--------------------------------------------- Readme
// This structure only support single-producer and signle-consumer
//--------------------------------------------- Readme

#ifndef MSG_Q_LOCKFREE_LINKLIST_STD_H
#define MSG_Q_LOCKFREE_LINKLIST_STD_H
#include "MsgQBase.h"
#include "Logger.h"

#include <atomic>
#include <thread>
#include <mutex>
#include <condition_variable>

template<typename T>
class MsgQLockFree_LinkList_Std : public MsgQBase<T>
{
 private:
    struct node
    {
        std::shared_ptr<T> data;
        node* next;

        node ()
            : next(nullptr)
        {}
    };
 public:
    MsgQLockFree_LinkList_Std()
        : m_head(new node)
        , m_tail(m_head.load())
    {
        LOGMSG_CLASS_NAME("MsgQLockFree_LinkList_Std");
    }
    ~MsgQLockFree_LinkList_Std()
    {
        while (node *const oldHead = m_head.load())
        {
            m_head.store(oldHead->next);
            delete oldHead;
        }
    }
    MsgQLockFree_LinkList_Std (const MsgQLockFree_LinkList_Std& other) = delete;
    MsgQLockFree_LinkList_Std& operator= (const MsgQLockFree_LinkList_Std& other) = delete;

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
    node* popHead()
    {
        node *const oldHead = m_head.load();
        if (oldHead == m_tail.load())
        {
            return nullptr;
        }
        m_head.store(oldHead->next);
        return oldHead;
    }
 private:
    std::atomic<node*> m_head;
    std::atomic<node*> m_tail;
};

// override MsgQBase<T>
template<typename T>
bool MsgQLockFree_LinkList_Std<T>::AddMsg(std::shared_ptr<T>& msg)
{
    node *p = new node;
    node *const oldTail = m_tail.load();
    oldTail->data.swap(msg);
    oldTail->next = p;
    m_tail.store(p);

    return true;
}
// override MsgQBase<T>
template<typename T>
bool MsgQLockFree_LinkList_Std<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    node *p = new node;
    node *const oldTail = m_tail.load();
    oldTail->data.swap(msg);
    oldTail->next = p;
    m_tail.store(p);

    return true;
}
// override MsgQBase<T>
template<typename T>
void MsgQLockFree_LinkList_Std<T>::GetMsg(std::shared_ptr<T>& msg)
{
    node * oldHead = popHead();
    if (!oldHead)
    {
        msg = std::shared_ptr<T>();
        return;
    }

    msg.swap(oldHead->data);
    delete oldHead;
}
// override MsgQBase<T>
template<typename T>
int MsgQLockFree_LinkList_Std<T>::GetMsgNum()
{
    return 0;
}
// override MsgQBase<T>
template<typename T>
void MsgQLockFree_LinkList_Std<T>::Flush()
{
}
// override MsgQBase<T>
template<typename T>
std::string MsgQLockFree_LinkList_Std<T>::GetQName()
{
    return "MsgQLockFree_LinkList_Std";
}

#endif
