#ifndef RM_ARRAY_H
#define RM_ARRAY_H
#include <stdint.h>

template<typename T>
class RM_Array
{
 public:
    RM_Array();
    RM_Array(uint32_t count);
    ~RM_Array();

    uint32_t GetSize();
    uint32_t GetCapacity();
    void Clear();
 private:
    static inline uint32_t RoundUpPowOfTwo(uint32_t x);
 private:
    T *m_pHead;
    uint32_t m_size;
    uint32_t m_capacity;
};

template<typename T>
RM_Array<T>::RM_Array()
{
    m_size = 0;
    m_capacity = 0;
    m_pHead = nullptr;
}

template<typename T>
RM_Array<T>::RM_Array(uint32_t count)
{
    m_size = 0;
    m_capacity = count;
    m_pHead = new T[count];
}

template<typename T>
RM_Array<T>::~RM_Array()
{
    Clear();
}

template<typename T>
uint32_t RM_Array<T>::GetSize()
{
    return m_size;
}

template<typename T>
void RM_Array<T>::Clear()
{
    if (m_size > 0 || m_pHead)
        delete m_pHead;
    m_pHead = nullptr;
    m_size = 0;
}

template<typename T>
inline uint32_t RM_Array<T>::RoundUpPowOfTwo(uint32_t x)
{
    if (x == 0) return 1;

    x--;
    int count = 0;
    while (x > 0)
    {
        x >>= 1;
        count++;
    }

    if (count >= 32) count = 31;
    return 1 << count;
}
#endif
