#ifndef STD_CLASS_WITH_THREAD_H
#define STD_CLASS_WITH_THREAD_H
#include "StdThread.h"

class StdClassWithThread : public StdThread
{
 public:
    StdClassWithThread();
    ~StdClassWithThread();

    bool InitComponent();
 private:
    // override
    void* Main();
};

#endif
