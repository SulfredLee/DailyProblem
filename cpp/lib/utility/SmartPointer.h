#ifndef SMARTPOINTER_H
#define SMARTPOINTER_H

#include <iostream>
#include "DefaultMutex.h"

class ReferenceCount
{
 public:
    ReferenceCount();
    ~ReferenceCount();

    void AddRef();
    int Release();
 private:
    int m_count;
    DefaultMutex m_mutex;
};

template<typename T>
class SmartPointer
{
 public:
    SmartPointer();
    SmartPointer(T* pData);
    SmartPointer(const SmartPointer<T>& smartPointer);
    template<typename U>
        SmartPointer(const SmartPointer<U>& smartPointer, T* pData);
    ~SmartPointer();

    T& operator* ();
    T* operator-> ();
    SmartPointer<T>& operator = (const SmartPointer<T>& smartPointer);

    T* Get();
    T* Get() const;

    template<typename> friend class SmartPointer; // with this friend, we can define the following constructor, SmartPointer(const SmartPointer<U>& smartPointer, T* pData)
 private:
    T* m_pData;
    ReferenceCount* m_pRC;
};

template<typename T>
SmartPointer<T> MakeSmartPointer();

template<typename T, typename U>
    SmartPointer<T> StaticCast(const SmartPointer<U>& smartPointer);

template<typename T, typename U>
    SmartPointer<T> DynamicCast(const SmartPointer<U>& smartPointer);

//////////////////////////////////////////////////////////////////////////////////
// Start implementation
//////////////////////////////////////////////////////////////////////////////////

template<typename T>
SmartPointer<T>::SmartPointer()
    : m_pData(NULL), m_pRC(NULL)
{
    m_pRC = new ReferenceCount();
}

template<typename T>
SmartPointer<T>::SmartPointer(T* pData)
    : m_pData(pData), m_pRC(NULL)
{
    m_pRC = new ReferenceCount();
    m_pRC->AddRef();
}

template<typename T>
SmartPointer<T>::SmartPointer(const SmartPointer<T>& smartPointer)
    : m_pData(smartPointer.m_pData), m_pRC(smartPointer.m_pRC)
{
    m_pRC->AddRef();
}

template<typename T>
template<typename U>
SmartPointer<T>::SmartPointer(const SmartPointer<U>& smartPointer, T* pData)
    : m_pData(pData), m_pRC(smartPointer.m_pRC)
{
    m_pRC->AddRef();
}

template<typename T>
SmartPointer<T>::~SmartPointer()
{
    if (m_pRC->Release() == 0)
    {
        if (m_pData)
            delete m_pData;
        delete m_pRC;
    }
}

template<typename T>
T& SmartPointer<T>::operator* ()
{
    return *m_pData;
}

template<typename T>
T* SmartPointer<T>::operator-> ()
{
    return m_pData;
}

template<typename T>
SmartPointer<T>& SmartPointer<T>::operator = (const SmartPointer<T>& smartPointer)
{
    if (this != &smartPointer)
    {
        if (m_pRC->Release() == 0)
        {
            if (m_pData)
                delete m_pData;
            delete m_pRC;
        }

        m_pData = smartPointer.m_pData;
        m_pRC = smartPointer.m_pRC;
        m_pRC->AddRef();
    }
    return *this;
}

template<typename T>
T* SmartPointer<T>::Get()
{
    return m_pData;
}

template<typename T>
T* SmartPointer<T>::Get() const
{
 return m_pData;
}

template<typename T>
SmartPointer<T> MakeSmartPointer()
{
    SmartPointer<T> smartPointer(new T());
    return smartPointer;
}

template<typename T, typename U>
SmartPointer<T> StaticCast(const SmartPointer<U>& smartPointer)
{
    T* p = static_cast<T*>(smartPointer.Get());
    return SmartPointer<T>(smartPointer, p);
}

template<typename T, typename U>
SmartPointer<T> DynamicCast(const SmartPointer<U>& smartPointer)
{
    T* p = dynamic_cast<T*>(smartPointer.Get());
    if (p)
        return SmartPointer<T>(smartPointer, p);
    else
        return SmartPointer<T>();
}

#endif
