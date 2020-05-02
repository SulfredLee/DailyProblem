#include <iostream>
#include "allFood.h"

int main(int argc, char *argv[])
{
    food* pApple = createApple();
    ((apple*)pApple)->nNumber = 10;
    pApple->printName("001");
    fprintf(stdout, "We have %d apples.\n", ((apple*)pApple)->nNumber);
    food* pOrange = createOrange();
    pOrange->printName("002");
    return 0;
}
