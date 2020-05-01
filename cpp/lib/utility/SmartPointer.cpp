#include "SmartPointer.h"

ReferenceCount::ReferenceCount()
{
    m_count = 0;
}

ReferenceCount::~ReferenceCount()
{
}

void ReferenceCount::AddRef()
{
    DefaultLock lock(m_mutex);
    m_count++;
}

int ReferenceCount::Release()
{
    DefaultLock lock(m_mutex);
    if (m_count > 0)
    {
        return --m_count;
    }
    else
    {
        m_count = 0;
        return m_count;
    }
}
