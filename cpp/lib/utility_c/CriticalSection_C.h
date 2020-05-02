#ifndef CRITICALSECTION_C_H
#define CRITICALSECTION_C_H

#ifdef __cplusplus
extern "C"
{
#endif
    struct CriticalSection_C;
    struct CriticalSection_C* createCriticalSection_C();
    void freeCriticalSection_C(struct CriticalSection_C** inMutex);

    void Lock_CriticalSection_C(struct CriticalSection_C* inMutex);
    void Unlocak_CriticalSection_C(struct CriticalSection_C* inMutex);
#ifdef __cplusplus
};
#endif
#endif
