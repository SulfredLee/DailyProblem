#ifndef MSG_Q_ONELOCK_QUEUE_LINUX_H
#define MSG_Q_ONELOCK_QUEUE_LINUX_H
#include "DefaultMutex.h"
#include "MsgQBase.h"
#include "Logger.h"

#include <atomic>
#include <thread>
#include <queue>

template<typename T>
class MsgQOneLock_Queue_Linux : public MsgQBase<T>
{
 private:
    struct node
    {
        std::shared_ptr<T> data;
        std::unique_ptr<node> next;
    };
 public:
    MsgQOneLock_Queue_Linux()
    {
        LOGMSG_CLASS_NAME("MsgQOneLock_Queue_Linux");
        pthread_cond_init(&m_cond, NULL);
    }
    ~MsgQOneLock_Queue_Linux()
    {
        pthread_cond_destroy(&m_cond);
    }
    MsgQOneLock_Queue_Linux (const MsgQOneLock_Queue_Linux& other) = delete;
    MsgQOneLock_Queue_Linux& operator= (const MsgQOneLock_Queue_Linux& other) = delete;

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
    std::queue<std::shared_ptr<T> > m_msgQ;
};

// override MsgQBase<T>
template<typename T>
bool MsgQOneLock_Queue_Linux<T>::AddMsg(std::shared_ptr<T>& msg)
{
    {
        DefaultLock lock(m_mutex);
        m_msgQ.push(std::move(msg));
    }
    pthread_cond_signal(&m_cond);
    return true;
}

// override MsgQBase<T>
template<typename T>
bool MsgQOneLock_Queue_Linux<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    {
        DefaultLock lock(m_mutex);
        m_msgQ.push(std::move(msg));
    }
    pthread_cond_signal(&m_cond);
    return true;
}

// override MsgQBase<T>
template<typename T>
void MsgQOneLock_Queue_Linux<T>::GetMsg(std::shared_ptr<T>& msg)
{
    pthread_mutex_lock(m_mutex.GetMutex());
    while (m_msgQ.size() == 0)
    {
        pthread_cond_wait(&m_cond, m_mutex.GetMutex());
    }
    msg = m_msgQ.front();
    m_msgQ.pop();
    pthread_mutex_unlock(m_mutex.GetMutex());
}

// override MsgQBase<T>
template<typename T>
int MsgQOneLock_Queue_Linux<T>::GetMsgNum()
{
    return m_msgQ.size();
}

// override MsgQBase<T>
template<typename T>
void MsgQOneLock_Queue_Linux<T>::Flush()
{
}

// override MsgQBase<T>
template<typename T>
std::string MsgQOneLock_Queue_Linux<T>::GetQName()
{
    return "MsgQOneLock_Queue_Linux";
}
#endif
