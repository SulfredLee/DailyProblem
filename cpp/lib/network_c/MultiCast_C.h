#ifndef MULTICAST_C_H
#define MULTICAST_C_H

#ifdef __cplusplus
extern "C"
{
#endif
    enum MCStatus {SUCCESS, ERROR, READ};
    struct MCast_C;
    struct MCast_C* createMCast_C();
    void freeMCast_C(struct MCast_C** pMCast);

    enum MCStatus MCast_C_InitComponent(struct MCast_C* pMCast, char const * const ifAddress, int ifAddressLen, short ifPort);
    // Set time to live
    enum MCStatus MCast_C_SetTTL(struct MCast_C* pMCast, int ttl);

    // Client
    // Join the multicast group to receive datagrams.
    enum MCStatus MCast_C_JoinGroup(struct MCast_C* pMCast, char const * const grpAddress, int grpAddressLen);
    // Leave the multicast group
    enum MCStatus MCast_C_LeaveGroup(struct MCast_C* pMCast, char const * const grpAddress, int grpAddressLen);
    // Receive data from the multicasting group server.
    enum MCStatus MCast_C_SelectRead(struct MCast_C* pMCast, long uSec, long sec);
    enum MCStatus MCast_C_Recv(struct MCast_C* pMCast, char* receiveBuffer, int receiveBufferLen, char* fromAddress, int* fromAddressLen, short* fromPort, int* byteRecv);

    // Server
    // Send a message to the multicasting address with specified port.
    enum MCStatus MCast_C_Send(struct MCast_C* pMCast, char* toAddress, int toAddressLen, char const * const sendMsg, const int msgLength);

    // private
    static enum MCStatus MCast_C_Start(struct MCast_C* pMCast);
    static void MCast_C_Stop(struct MCast_C* pMCast);
#ifdef __cplusplus
};
#endif
#endif
