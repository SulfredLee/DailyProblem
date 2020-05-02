#ifndef ALL_FOOD_H
#define ALL_FOOD_H
#ifdef __cplusplus
extern "C"
{
#endif

#include "food.h"

typedef struct{
    printNameFun printName;
    int nNumber;
} apple;

food* createApple();

typedef struct{
    printNameFun printName;
    int nPrice;
} orange;

food* createOrange();
#ifdef __cplusplus
};
#endif
#endif
