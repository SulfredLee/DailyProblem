#include <iostream>
#include "RM_Array.h"

uint32_t RoundUpPowOfTwo(uint32_t x)
{
    if (x == 0) return 1;

    x--;
    int count = 0;
    while (x > 0)
    {
        x >>= 1;
        count++;
    }

    if (count >= 32) count = 31;
    return 1 << count;
}
int main(int argc, char *argv[])
{
    RM_Array<int> numbers(10);
    std::cout << numbers.GetSize() << std::endl;
    numbers.Clear();

    std::cout << RoundUpPowOfTwo(0x80000000) << std::endl;
    std::cout << 0x80000000 << std::endl;
    return 0;
}
