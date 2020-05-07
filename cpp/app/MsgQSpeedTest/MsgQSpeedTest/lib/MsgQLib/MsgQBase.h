#ifndef MSG_Q_BASE_H
#define MSG_Q_BASE_H

#include <memory>
#include <string>

#define MAX_MSG_NUM 524288

template<typename T>
class MsgQBase
{
 public:
    MsgQBase() {}
    virtual ~MsgQBase() {}

    virtual bool AddMsg(std::shared_ptr<T>& msg) = 0;
    virtual bool AddMsg(std::shared_ptr<T>&& msg) = 0;
    virtual void GetMsg(std::shared_ptr<T>& msg) = 0;
    virtual int GetMsgNum() = 0;
    virtual void Flush() = 0;
    virtual std::string GetQName() = 0;
};

#endif
