#include <iostream>
#include <functional>
#include "Cat_A.h"


int main(int argc, char* argv[])
{
    CatA cat;
    // bind a child function case
    std::function<void(const std::string&)> xx = std::bind(&CatA::PrintName, &cat, std::placeholders::_1);
    xx("tempCat");

    // bind a static function case
    std::function<int(const int)> yy = std::bind(&CatA::PrintBaseName, std::placeholders::_1);
    yy(10);

    return 0;
}
