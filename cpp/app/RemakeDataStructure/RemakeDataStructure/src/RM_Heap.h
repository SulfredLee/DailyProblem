#ifndef RM_HEAP_H
#define RM_HEAP_H
#include <iostream>

namespace RM
{
    template <class RandomAccessIterator, class Distance, class T>
        void __PushHeap (RandomAccessIterator first, Distance holeIndex, Distance topIndex, T value)
    {
        // percolate up
        Distance parent = (holeIndex - 1) / 2; // find father node
        while (holeIndex > topIndex && *next(first, parent) < value)
        {
            *(first + holeIndex) = *(first + parent);
            holeIndex = parent;
            parent = (holeIndex - 1) / 2;
        }
        *(first + holeIndex) = value;
    }
    template<class T>
        void __PushHeapAux(T first, T last, std::random_access_iterator_tag)
    {
        __PushHeap(first, distance(first, prev(last)), distance(first, first), *prev(last));
    }
    template<class T>
        void PushHeap(T first, T last)
    {
        typename std::iterator_traits<T>::iterator_category t;
        __PushHeapAux(first, last, t);
    }
    template <class RandomAccessIterator, class Distance, class T>
        void __AdjustHeap (RandomAccessIterator first, Distance holeIndex, Distance len, T value)
    {
        // percolate down
        Distance topIndex = holeIndex;
        Distance secondChild = 2 * holeIndex + 2;
        while (secondChild < len)
        {
            if (*(first + secondChild) < *(first + (secondChild - 1)))
                secondChild--;
            *(first + holeIndex) = *(first + secondChild);
            holeIndex = secondChild;
            secondChild = 2 * (secondChild + 1);
        }
        if (secondChild == len) // only left child case
        {
            *(first + holeIndex) = *(first + (secondChild - 1));
            holeIndex = secondChild - 1;
        }
        __PushHeap (first, holeIndex, topIndex, value);
    }
    template <class RandomAccessIterator, class T>
        void __PopHeap (RandomAccessIterator first, RandomAccessIterator last, RandomAccessIterator result, T value)
    {
        *result = *first;
        __AdjustHeap(first, distance(first, first), distance(first, last), value);
    }
    template<class T>
        void __PopHeapAux(T first, T last, std::random_access_iterator_tag)
    {
        __PopHeap(first, prev(last), prev(last), *prev(last));
    }
    template<class T>
        void PopHeap(T first, T last)
    {
        typename std::iterator_traits<T>::iterator_category t;
        __PopHeapAux(first, last, t);
    }
    template <class RandomAccessIterator>
        void SortHeap (RandomAccessIterator first, RandomAccessIterator last)
    {
        while (last - first > 1)
            PopHeap(first, last--);
    }
    template <class T>
        void __MakeHeap (T first, T last, std::random_access_iterator_tag)
    {
        if (last - first < 2) return;
        auto len = distance(first, last);
        auto holeIndex = (len - 2) / 2;

        while (true)
        {
            __AdjustHeap(first, holeIndex, len, *next(first, holeIndex));
            if (holeIndex == 0) return;
            holeIndex--;
        }
    }
    template <class T>
        inline void MakeHeap (T first, T last)
    {
        typename std::iterator_traits<T>::iterator_category t;
        __MakeHeap(first, last, t);
    }
};
#endif
