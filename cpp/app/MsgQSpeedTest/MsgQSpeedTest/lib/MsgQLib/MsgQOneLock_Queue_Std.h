#ifndef MSG_Q_ONELOCK_QUEUE_STD_H
#define MSG_Q_ONELOCK_QUEUE_STD_H
#include "MsgQBase.h"
#include "Logger.h"

#include <atomic>
#include <thread>
#include <mutex>
#include <condition_variable>

template<typename T>
class MsgQOneLock_Queue_Std : public MsgQBase<T>
{
 private:
    struct node
    {
        std::shared_ptr<T> data;
        std::unique_ptr<node> next;
    };
 public:
    MsgQOneLock_Queue_Std()
    {
        LOGMSG_CLASS_NAME("MsgQOneLock_Queue_Std");
    }
    ~MsgQOneLock_Queue_Std()
    {
    }
    MsgQOneLock_Queue_Std (const MsgQOneLock_Queue_Std& other) = delete;
    MsgQOneLock_Queue_Std& operator= (const MsgQOneLock_Queue_Std& other) = delete;

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
    std::queue<std::shared_ptr<T> > m_msgQ;
};

// override MsgQBase<T>
template<typename T>
bool MsgQOneLock_Queue_Std<T>::AddMsg(std::shared_ptr<T>& msg)
{
    {
        std::lock_guard<std::mutex> lock(m_mutex);
        m_msgQ.push(std::move(msg));
    }
    m_cond.notify_one();
    return true;
}

// override MsgQBase<T>
template<typename T>
bool MsgQOneLock_Queue_Std<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    {
        std::lock_guard<std::mutex> lock(m_mutex);
        m_msgQ.push(std::move(msg));
    }
    m_cond.notify_one();
    return true;
}

// override MsgQBase<T>
template<typename T>
void MsgQOneLock_Queue_Std<T>::GetMsg(std::shared_ptr<T>& msg)
{
    std::unique_lock<std::mutex> lock(m_mutex);
    m_cond.wait(lock, [&] { return m_msgQ.size() != 0; });
    msg = m_msgQ.front();
    m_msgQ.pop();
}

// override MsgQBase<T>
template<typename T>
int MsgQOneLock_Queue_Std<T>::GetMsgNum()
{
    return m_msgQ.size();
}

// override MsgQBase<T>
template<typename T>
void MsgQOneLock_Queue_Std<T>::Flush()
{
}

// override MsgQBase<T>
template<typename T>
std::string MsgQOneLock_Queue_Std<T>::GetQName()
{
    return "MsgQOneLock_Queue_Std";
}
#endif
