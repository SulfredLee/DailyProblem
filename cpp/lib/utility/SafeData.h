#ifndef SAFE_DATA_H
#define SAFE_DATA_H
#include "DefaultMutex.h"

template<typename T>
class SafeData
{
 public:
    SafeData();
    ~SafeData();

    void SetValue(T inData);
    T GetValue();
 private:
    T m_data;
    DefaultMutex m_mutex;
};

template<typename T>
SafeData<T>::SafeData()
{
}

template<typename T>
SafeData<T>::~SafeData()
{
}

template<typename T>
void SafeData<T>::SetValue(T inData)
{
    DefaultLock lock(m_mutex);
    m_data = inData;
}

template<typename T>
T SafeData<T>::GetValue()
{
    DefaultLock lock(m_mutex);
    return m_data;
}
#endif
