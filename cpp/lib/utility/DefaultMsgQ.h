#ifndef DEFAULT_MSG_Q_H
#define DEFAULT_MSG_Q_H
#include "DefaultMutex.h"
#include "SmartPointer.h"

#include <queue>

template<typename T>
class DefaultMsgQ
{
 public:
    DefaultMsgQ();
    ~DefaultMsgQ();

    void InitComponent();
    bool AddMsg(SmartPointer<T>& msg);
    bool AddMsg(SmartPointer<T>&& msg);
    void GetMsg(SmartPointer<T>& msg);
    int GetMsgNum();
    void Flush();
 private:
    DefaultMutex m_mutex;
    pthread_cond_t m_cond;
    std::queue<SmartPointer<T> > m_msgQ;
};

template<typename T>
DefaultMsgQ<T>::DefaultMsgQ()
{
    pthread_cond_init(&m_cond, NULL);
}

template<typename T>
DefaultMsgQ<T>::~DefaultMsgQ()
{
    pthread_cond_destroy(&m_cond);
}

template<typename T>
void DefaultMsgQ<T>::InitComponent()
{
}

template<typename T>
bool DefaultMsgQ<T>::AddMsg(SmartPointer<T>& msg)
{
    DefaultLock lock(m_mutex);
    m_msgQ.push(std::move(msg));
    pthread_cond_signal(&m_cond);
    return true;
}

template<typename T>
bool DefaultMsgQ<T>::AddMsg(SmartPointer<T>&& msg)
{
    DefaultLock lock(m_mutex);
    m_msgQ.push(std::move(msg));
    pthread_cond_signal(&m_cond);
    return true;
}

template<typename T>
void DefaultMsgQ<T>::GetMsg(SmartPointer<T>& msg)
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
int DefaultMsgQ<T>::GetMsgNum()
{
    DefaultLock lock(m_mutex);
    return m_msgQ.size();
}

template<typename T>
void DefaultMsgQ<T>::Flush()
{
    DefaultLock lock(m_mutex);
    std::queue<SmartPointer<T> > empty;
    std::swap(m_msgQ, empty);
}

#endif
