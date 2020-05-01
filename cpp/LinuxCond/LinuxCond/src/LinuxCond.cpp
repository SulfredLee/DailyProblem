#include "LinuxCond.h"

#include <sys/time.h>
LinuxCond::LinuxCond()
{
    pthread_cond_init(&m_cond, NULL);
}

LinuxCond::~LinuxCond()
{
    pthread_cond_destroy(&m_cond);
}

void LinuxCond::Signal()
{
    DefaultLock lock(m_mutex);
    pthread_cond_signal(&m_cond);
}

int LinuxCond::WaitWithTime(int MSec)
{
    pthread_mutex_lock(m_mutex.GetMutex());

    struct timespec ts;
    struct timeval tv;
    gettimeofday(&tv, NULL);
    ts.tv_sec = tv.tv_sec;
    ts.tv_nsec = tv.tv_usec * 1000;
    ts.tv_sec += MSec / 1000;
    ts.tv_nsec += 1000 * 1000 * (MSec % 1000);
    ts.tv_sec += ts.tv_nsec / (1000 * 1000 * 1000);
    ts.tv_nsec %= (1000 * 1000 * 1000);

    int ret = pthread_cond_timedwait(&m_cond, m_mutex.GetMutex(), &ts);

    pthread_mutex_unlock(m_mutex.GetMutex());

    return ret;
}

int LinuxCond::Wait()
{
    pthread_mutex_lock(m_mutex.GetMutex());
    int ret = pthread_cond_wait(&m_cond, m_mutex.GetMutex());
    pthread_mutex_unlock(m_mutex.GetMutex());
    return ret;
}
