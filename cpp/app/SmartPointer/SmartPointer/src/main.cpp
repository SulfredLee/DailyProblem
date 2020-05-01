#include <iostream>

#include "SmartPointer.h"

class Foo
{
public:
    Foo() { std::cout << "Hello from constructor" << std::endl; }
    ~Foo() { std::cout << "Hello from destructor" << std::endl; }

    void Print() { std::cout << "Hello from Foo" << std::endl; }
};
class BaseClass
{
public:
    BaseClass() { std::cout << "Hello from BaseClass constructor" << std::endl; }
    virtual ~BaseClass() { std::cout << "Hello from BaseClass destructor" << std::endl; }

    virtual void Print() {}
};
class ChildClass : public BaseClass
{
public:
    ChildClass() { std::cout << "Hello from ChildClass constructor" << std::endl; }
    ~ChildClass() { std::cout << "Hello from ChildClass destructor" << std::endl; }

    // override
    void Print() { std::cout << "Hello from ChildClass Print" << std::endl; }
};

void SimpleCase()
{
    {
        SmartPointer<Foo> foo = MakeSmartPointer<Foo>();
        foo->Print();
    }
    std::cout << "Hello from END" << std::endl;
}
void InheritCase_Print(SmartPointer<BaseClass> p)
{
    SmartPointer<BaseClass> pp = p;
    pp->Print();
    std::cout << "Hello from END" << std::endl;
}
void InheritCase()
{
    std::cout << std::endl;
    SmartPointer<BaseClass> base = StaticCast<BaseClass>(MakeSmartPointer<ChildClass>());
    InheritCase_Print(base);
    std::cout << "Hello from END" << std::endl;
}
int main (int argc, char *argv[])
{
    SimpleCase();
    InheritCase();

    return 0;
}
