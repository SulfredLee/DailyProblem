#ifndef CAT_A_H
#define CAT_A_H
#include "CatBase.h"

class CatA : public CatBase
{
 public:
    CatA();
    ~CatA();

    void PrintName(const std::string& fakeName) override;
};

#endif
