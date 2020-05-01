#include <iostream>
#include <thread>
#include <chrono>

#include "MsgQ.h"
#include "DefaultMsgQ.h"

class BaseMsg
{
public:
    BaseMsg() {}
    virtual ~BaseMsg() {}

    void SetCount(int count) { m_count = count; }
    int GetCount() { return m_count; }
protected:
    int m_count;
};
class ChildMsg : public BaseMsg
{
public:
    ChildMsg() {}
    ~ChildMsg() {}
};

MsgQ<BaseMsg> m_msgQ;
void PushWorker()
{
    for (int i = 0; i < 3; i++)
    {
        std::shared_ptr<BaseMsg> msg = std::make_shared<ChildMsg>();
        msg->SetCount(i);
        m_msgQ.AddMsg(msg);
        std::cout << "Add Msg: " << i << std::endl;
    }
}
void PullWorker()
{
    int count = 0;
    while (count < 2)
    {
        std::shared_ptr<BaseMsg> msg;
        m_msgQ.GetMsg(msg);
        count = msg->GetCount();
        std::cout << "Get Msg: " << count << std::endl;
    }
}

DefaultMsgQ<BaseMsg> m_defaultMsgQ;
void PushWorker_Default()
{
    for (int i = 0; i < 3; i++)
    {
        SmartPointer<BaseMsg> msg = StaticCast<BaseMsg>(MakeSmartPointer<ChildMsg>());
        msg->SetCount(i);
        m_defaultMsgQ.AddMsg(msg);
        std::cout << "Add Msg: " << i << std::endl;
    }
}
void PullWorker_Default()
{
    int count = 0;
    while (count < 2)
    {
        SmartPointer<BaseMsg> msg;
        m_defaultMsgQ.GetMsg(msg);
        count = msg->GetCount();
        std::cout << "Get Msg: " << count << std::endl;
    }
}
int main(int argc, char *argv[])
{
    std::cout << "Msg Q example." << std::endl;
    std::thread pushTH(PushWorker);
    pushTH.detach();
    std::this_thread::sleep_for(std::chrono::seconds(1));
    std::thread pullTH(PullWorker);
    pullTH.detach();
    std::this_thread::sleep_for(std::chrono::seconds(1));

    std::cout << std::endl;
    std::cout << "Default Msg Q example." << std::endl;
    std::thread pushTH_Default(PushWorker_Default);
    pushTH_Default.detach();
    std::this_thread::sleep_for(std::chrono::seconds(1));
    std::thread pullTH_Default(PullWorker_Default);
    pullTH_Default.detach();
    std::this_thread::sleep_for(std::chrono::seconds(1));

    return 0;
}
