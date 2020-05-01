#include "LinuxThread.h"

LinuxThread::LinuxThread()
{
    m_run.SetValue(false);
    m_thread = 0;
}

LinuxThread::~LinuxThread()
{
    stopThread();
    if (m_thread) pthread_join(m_thread, NULL);
}

bool LinuxThread::startThread()
{
    m_run.SetValue(true);
    int ret = pthread_create(&m_thread, NULL, LinuxThread::MainProxy, (void*)this);
    if (ret)
    {
        // LOGMSG_ERROR("pthread_create fail, code: %d", ret);
        return false;
    }
    return true;
}

bool LinuxThread::isThreadRunning()
{
    return m_run.GetValue();
}

void LinuxThread::stopThread()
{
    m_run.SetValue(false);
}

void LinuxThread::joinThread()
{
    if (m_thread) pthread_join(m_thread, NULL);
    m_thread = 0;
}

void* LinuxThread::MainProxy(void* context)
{
    return ((LinuxThread* )context)->Main();
}
