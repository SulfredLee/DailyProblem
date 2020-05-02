#ifndef MSGQ_C_H
#define MSGQ_C_H
#ifdef __cplusplus
extern "C"
{
#endif
    struct MsgQ_C;
    struct MsgQ_C* createMsgQ_C();
    void freeMsgQ_C(struct MsgQ_C* inQueue);
    int pushMsgQ_C(void** inData, struct MsgQ_C* inQueue);
    int getMsgQ_C(void ** outData, struct MsgQ_C* inQueue);
#ifdef __cplusplus
};
#endif
#endif
