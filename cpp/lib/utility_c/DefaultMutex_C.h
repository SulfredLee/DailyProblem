#ifndef DEFAULTMUTEX_C_H
#define DEFAULTMUTEX_C_H

#ifdef __cplusplus
extern "C"
{
#endif
    struct DefaultMutex_C;
    struct DefaultMutex_C* createDefaultMutex_C();
    void freeDefaultMutex_C(struct DefaultMutex_C** inMutex);

    void Lock_DefaultMutex_C(struct DefaultMutex_C* inMutex);
    void Unlocak_DefaultMutex_C(struct DefaultMutex_C* inMutex);
#ifdef __cplusplus
};
#endif
#endif
