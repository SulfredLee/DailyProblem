#ifndef UDPCAST_C_H
#define UDPCAST_C_H

#include "DefaultMutex_C.h"

#ifdef __cplusplus
extern "C"
{
#endif
    enum UDPStatus {SUCCESS, ERROR, READ};
    struct UDPCast_C;
    struct UDPCast_C* createUDPCast_C();
    void freeUDPCast_C(struct UDPCast_C** pUDPCast);

    enum UDPStatus UDPCast_C_InitComponent(struct UDPCast_C* pUDPCast, char const * const ifAddress, int ifAddressLen, short ifPort, int isClient);
    // Set time to live
    enum UDPStatus UDPCast_C_SetTTL(struct UDPCast_C* pUDPCast, int ttl);

    // Client, Server
    enum UDPStatus UDPCast_C_Send(struct UDPCast_C* pUDPCast, char const * const toAddress, int toAddressLen, short toPort, char const * const sendMsg, int msgLength);
    enum UDPStatus UDPCast_C_SelectRead(struct UDPCast_C* pUDPCast, long uSec, long sec);
    enum UDPStatus UDPCast_C_Recv(struct UDPCast_C* pUDPCast, char* fromAddress, int* fromAddressLen, short* fromPort, char* receiveBuffer, int receiveBufferLen, int* byteRecv);

    // private
    static enum UDPStatus UDPCast_C_Start(struct UDPCast_C* pUDPCast);
    static void UDPCast_C_Stop(struct UDPCast_C* pUDPCast);
#ifdef __cplusplus
};
#endif
#endif
