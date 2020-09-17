#ifndef CAT_BASE_H
#define CAT_BASE_H
#include <string>

class CatBase
{
 public:
    CatBase();
    ~CatBase();

    virtual void PrintName(const std::string& fakeName);
    static int PrintBaseName(const int id);
};

#endif
