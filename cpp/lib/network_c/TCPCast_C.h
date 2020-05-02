#ifndef TCPCAST_C_H
#define TCPCAST_C_H

#ifdef __cplusplus
extern "C"
{
#endif
    enum TCPStatus {SUCCESS, ERROR, READ};
    struct TCPCast_C;
    struct TCPCast_C* createTCPCast_C();
    void freeTCPCast_C(struct TCPCast_C** pTCPCast);

    enum TCPStatus TCPCast_C_InitComponent(struct TCPCast_C* pTCPCast, char const * const ifAddress, int ifAddressLen, short ifPort, int isClient, const int numClients);

    // Client
    // Connect to TCP Server
    enum TCPStatus TCPCast_C_Connect(struct TCPCast_C* pTCPCast, char const * const toAddress, int toAddressLen, const short toPort);
    enum TCPStatus TCPCast_C_ClientSend(struct TCPCast_C* pTCPCast, char const * const sendMsg, const int msgLength);
    enum TCPStatus TCPCast_C_ClientRecv(struct TCPCast_C* pTCPCast, char* receiveBuffer, int receiveBufferLen, int* byteRecv);

    // Server
    // Wait for clients and return client handle
    int TCPCast_C_Accept(struct TCPCast_C* pTCPCast);
    enum TCPStatus TCPCast_C_ServerSend(struct TCPCast_C* pTCPCast, int clientHandle, char const * const sendMsg, const int msgLength);
    enum TCPStatus TCPCast_C_ServerRecv(struct TCPCast_C* pTCPCast, int clientHandle, char* receiveBuffer, int receiveBufferLen, int* byteRecv);

    // private
    static enum TCPStatus TCPCast_C_Start(struct TCPCast_C* pTCPCast);
    static void TCPCast_C_Stop(struct TCPCast_C* pTCPCast);
#ifdef __cplusplus
};
#endif
#endif
