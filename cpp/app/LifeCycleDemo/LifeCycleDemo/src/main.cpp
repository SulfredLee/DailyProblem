#include <iostream>

class ElemInBase
{
public:
    ElemInBase()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
    ~ElemInBase()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
};

class ElemInChild
{
public:
    ElemInChild()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
    ~ElemInChild()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
};

class BaseFoo
{
public:
    ElemInBase m_baseEle;
public:
    BaseFoo()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
    virtual ~BaseFoo()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
};

class FooA : public BaseFoo
{
public:
    ElemInChild m_childEle;
public:
    FooA()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
    ~FooA()
    {
        std::cout << __FUNCTION__ << std::endl;
    }
};

int main(int argc, char* argv[])
{
    FooA aa;

    return 0;
}
