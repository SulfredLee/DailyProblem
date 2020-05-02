#ifndef FOOD_H
#define FOOD_H
#ifdef __cplusplus
extern "C"
{
#endif

typedef void (*printNameFun)(const char* strIN);

typedef struct{
    printNameFun printName;
} food;
#ifdef __cplusplus
};
#endif
#endif
