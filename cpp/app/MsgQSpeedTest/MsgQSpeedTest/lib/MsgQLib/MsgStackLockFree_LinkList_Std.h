#ifndef MSG_STACK_LOCKFREE_LINKLIST_STD_H
#define MSG_STACK_LOCKFREE_LINKLIST_STD_H
#include "MsgQBase.h"
#include "Logger.h"

#include <atomic>
#include <thread>
#include <mutex>
#include <condition_variable>

template<typename T>
class MsgStackLockFree_LinkList_Std : public MsgQBase<T>
{
 private:
    struct node
    {
        std::shared_ptr<T> data;
        std::shared_ptr<node> next;

        node (std::shared_ptr<T> const& inData)
            : data(inData)
        {}
    };
 public:
    MsgStackLockFree_LinkList_Std()
    {
        LOGMSG_CLASS_NAME("MsgStackLockFree_LinkList_Std");
    }
    ~MsgStackLockFree_LinkList_Std()
    {
    }
    MsgStackLockFree_LinkList_Std (const MsgStackLockFree_LinkList_Std& other) = delete;
    MsgStackLockFree_LinkList_Std& operator= (const MsgStackLockFree_LinkList_Std& other) = delete;

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
    std::shared_ptr<node> m_head;
};

// override MsgQBase<T>
template<typename T>
bool MsgStackLockFree_LinkList_Std<T>::AddMsg(std::shared_ptr<T>& msg)
{
    std::shared_ptr<node> const newNode = std::make_shared<node>(msg);
    newNode->next = std::atomic_load(&m_head);
    while(!std::atomic_compare_exchange_weak(&m_head, &newNode->next, newNode));

    return true;
}
// override MsgQBase<T>
template<typename T>
bool MsgStackLockFree_LinkList_Std<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    std::shared_ptr<node> const newNode = std::make_shared<node>(msg);
    newNode->next = std::atomic_load(&m_head);
    while(!std::atomic_compare_exchange_weak(&m_head, &newNode->next, newNode));

    return true;
}
// override MsgQBase<T>
template<typename T>
void MsgStackLockFree_LinkList_Std<T>::GetMsg(std::shared_ptr<T>& msg)
{
    std::shared_ptr<node> oldHead = std::atomic_load(&m_head);
    while (oldHead && !std::atomic_compare_exchange_weak(&m_head, &oldHead, oldHead->next));
    msg = oldHead ? oldHead->data : std::shared_ptr<T>();
}
// override MsgQBase<T>
template<typename T>
int MsgStackLockFree_LinkList_Std<T>::GetMsgNum()
{
    return 0;
}
// override MsgQBase<T>
template<typename T>
void MsgStackLockFree_LinkList_Std<T>::Flush()
{
}
// override MsgQBase<T>
template<typename T>
std::string MsgStackLockFree_LinkList_Std<T>::GetQName()
{
    return "MsgStackLockFree_LinkList_Std";
}

#endif
