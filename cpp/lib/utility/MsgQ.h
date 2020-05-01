#ifndef MSG_Q_H
#define MSG_Q_H
#include "DefaultMutex.h"

#include <queue>
#include <memory>

template<typename T>
class MsgQ
{
 public:
    MsgQ();
    ~MsgQ();

    void InitComponent();
    bool AddMsg(std::shared_ptr<T>& msg);
    bool AddMsg(std::shared_ptr<T>&& msg);
    void GetMsg(std::shared_ptr<T>& msg);
    int GetMsgNum();
    void Flush();
 private:
    DefaultMutex m_mutex;
    pthread_cond_t m_cond;
    std::queue<std::shared_ptr<T> > m_msgQ;
};

template<typename T>
MsgQ<T>::MsgQ()
{
    pthread_cond_init(&m_cond, NULL);
}

template<typename T>
MsgQ<T>::~MsgQ()
{
    pthread_cond_destroy(&m_cond);
}

template<typename T>
void MsgQ<T>::InitComponent()
{
}

template<typename T>
bool MsgQ<T>::AddMsg(std::shared_ptr<T>& msg)
{
    DefaultLock lock(m_mutex);
    m_msgQ.push(std::move(msg));
    pthread_cond_signal(&m_cond);
    return true;
}

template<typename T>
bool MsgQ<T>::AddMsg(std::shared_ptr<T>&& msg)
{
    DefaultLock lock(m_mutex);
    m_msgQ.push(std::move(msg));
    pthread_cond_signal(&m_cond);
    return true;
}

template<typename T>
void MsgQ<T>::GetMsg(std::shared_ptr<T>& msg)
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

template<typename T>
int MsgQ<T>::GetMsgNum()
{
    DefaultLock lock(m_mutex);
    return m_msgQ.size();
}

template<typename T>
void MsgQ<T>::Flush()
{
    DefaultLock lock(m_mutex);
    std::queue<std::shared_ptr<T> > empty;
    std::swap(m_msgQ, empty);
}

#endif
