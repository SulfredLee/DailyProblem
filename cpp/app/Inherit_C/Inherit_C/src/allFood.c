#include "allFood.h"
#include <stdio.h>
#include <stdlib.h>

static void printAppleName(const char* strIN){
    fprintf(stdout, "I am an apple %s\n", strIN);
}

food* createApple(){
    apple* pApple = (apple*)malloc(sizeof(*pApple));
    pApple->printName = &printAppleName;
    return (food*)pApple;
}

static void printOrangeName(const char* strIN){
    fprintf(stdout, "I am an orange %s\n", strIN);
}

food* createOrange(){
    orange* pOrange = (orange*)malloc(sizeof(*pOrange));
    pOrange->printName = &printOrangeName;
    return (food*)pOrange;
}
