#include "CatBase.h"
#include <iostream>

CatBase::CatBase()
{
}

CatBase::~CatBase()
{
}

void CatBase::PrintName(const std::string& fakeName)
{
    std::cout << "This is CatBase" << std::endl;
}

int CatBase::PrintBaseName(const int id)
{
    std::cout << "This is CatBase: " << id << std::endl;
    return 0;
}
