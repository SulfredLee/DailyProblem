#ifndef NLTIME_C_H
#define NLTIME_C_H
#include <time.h>

#ifdef __cplusplus
extern "C"
{
#endif
    struct NLTime_C;
    struct NLTime_C* createNLTime_C();
    struct NLTime_C* stringCreateNLTime_C(const char* src, const char* fmt);
    struct NLTime_C* copyCreateNLTime_C(struct NLTime_C* other);
    void freeNLTime_C(struct NLTime_C** pTime);

    struct tm GetRawData(struct NLTime_C* pTime);
    time_t GetTimeT(struct NLTime_C* pTime);
    void SetCurrentTime(struct NLTime_C* pTime);
    void GetDate(struct NLTime_C* pTime, int* Y, int* Mon, int* D);
    void GetTime(struct NLTime_C* pTime, int* H, int* Min, int* S);

    void SetFromString(struct NLTime_C* pTime, const char* src, const char* fmt);

    void SetDate(struct NLTime_C* pTime, int Y, int Mon, int D);
    void SetTime(struct NLTime_C* pTime, int H, int Min, int S);

    void AddDate(struct NLTime_C* pTime, int Y, int Mon, int D);
    void AddTime(struct NLTime_C* pTime, int H, int Min, int S);

    int CompareNLTime_isSmaller(struct NLTime_C* first, struct NLTime_C* second);
    int CompareNLTime_isBigger(struct NLTime_C* first, struct NLTime_C* second);
    int CompareNLTime_isEqual(struct NLTime_C* first, struct NLTime_C* second);

    char* NLTime_toString(struct NLTime_C* pTime, const char* fmt);
#ifdef __cplusplus
};
#endif
#endif
