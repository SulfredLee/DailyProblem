#define _XOPEN_SOURCE // for strptime
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
// private
typedef struct NLTime_C
{
    struct tm m_time;
}NLTime_C;

// public
NLTime_C* createNLTime_C()
{
    NLTime_C* pTime = (NLTime_C*)malloc(sizeof(NLTime_C));
    mktime(&(pTime->m_time));
    return pTime;
}

NLTime_C* stringCreateNLTime_C(const char* src, const char* fmt)
{
    NLTime_C* pTime = (NLTime_C*)malloc(sizeof(NLTime_C));
    strptime(src, fmt, &(pTime->m_time));
    mktime(&(pTime->m_time));
    return pTime;
}

NLTime_C* copyCreateNLTime_C(struct NLTime_C* other)
{
    NLTime_C* pTime = (NLTime_C*)malloc(sizeof(NLTime_C));
    pTime->m_time = other->m_time;
    mktime(&(pTime->m_time));
    return pTime;
}

void freeNLTime_C(struct NLTime_C** pTime)
{
    free(*pTime);
    *pTime = NULL;
}

struct tm GetRawData(struct NLTime_C* pTime)
{
    return pTime->m_time;
}

time_t GetTimeT(struct NLTime_C* pTime)
{
    return mktime(&(pTime->m_time));
}

void SetCurrentTime(struct NLTime_C* pTime)
{
    time_t rawTime;
    time(&rawTime);
    pTime->m_time = *localtime(&rawTime);
}

void GetDate(struct NLTime_C* pTime, int* Y, int* Mon, int* D)
{
    *Y = pTime->m_time.tm_year + 1900;
    *Mon = pTime->m_time.tm_mon + 1;
    *D = pTime->m_time.tm_mday;
}

void GetTime(struct NLTime_C* pTime, int* H, int* Min, int* S)
{
    *H = pTime->m_time.tm_hour;
    *Min = pTime->m_time.tm_min;
    *S = pTime->m_time.tm_sec;
}

void SetFromString(struct NLTime_C* pTime, const char* src, const char* fmt)
{
    strptime(src, fmt, &(pTime->m_time));
    mktime(&(pTime->m_time));
}

void SetDate(struct NLTime_C* pTime, int Y, int Mon, int D)
{
    pTime->m_time.tm_year = Y - 1900;
    pTime->m_time.tm_mon = Mon - 1;
    pTime->m_time.tm_mday = D;
    mktime(&(pTime->m_time));
}

void SetTime(struct NLTime_C* pTime, int H, int Min, int S)
{
    pTime->m_time.tm_hour = H;
    pTime->m_time.tm_min = Min;
    pTime->m_time.tm_sec = S;
    mktime(&(pTime->m_time));
}

void AddDate(struct NLTime_C* pTime, int Y, int Mon, int D)
{
    pTime->m_time.tm_year += Y;
    pTime->m_time.tm_mon += Mon;
    pTime->m_time.tm_mday += D;
    mktime(&(pTime->m_time));
}

void AddTime(struct NLTime_C* pTime, int H, int Min, int S)
{
    pTime->m_time.tm_hour += H;
    pTime->m_time.tm_min += Min;
    pTime->m_time.tm_sec += S;
    mktime(&(pTime->m_time));
}

int CompareNLTime_isSmaller(struct NLTime_C* first, struct NLTime_C* second)
{
    return difftime(GetTimeT(first), GetTimeT(second)) < 0 ? 1 : 0;
}

int CompareNLTime_isBigger(struct NLTime_C* first, struct NLTime_C* second)
{
    return CompareNLTime_isSmaller(second, first);
}

int CompareNLTime_isEqual(struct NLTime_C* first, struct NLTime_C* second)
{
    return difftime(GetTimeT(first), GetTimeT(second)) == 0 ? 1 : 0;
}

char* NLTime_toString(struct NLTime_C* pTime, const char* fmt)
{
    char* buff = (char*)malloc(1024);
    strftime(buff, 1024, fmt, &(pTime->m_time));
    return buff;
}
