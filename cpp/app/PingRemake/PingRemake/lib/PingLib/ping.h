#ifndef PING_H
#define PING_H

#include <iostream>
#include <string>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <netinet/ip_icmp.h>
#include <time.h>
#include <fcntl.h>
#include <signal.h>
#include <time.h>

// Define the Packet Constants
// ping packet size
#define PING_PKT_S 64

// Automatic port number
#define PORT_NO 0

// Automatic port number
#define PING_SLEEP_RATE 1000000

// Gives the timeout delay for receiving packets
// in seconds
#define RECV_TIMEOUT 1

// ping packet structure
struct ping_pkt
{
    struct icmphdr hdr;
    char msg[PING_PKT_S-sizeof(struct icmphdr)];
};

class Ping
{
 public:
    Ping();
    ~Ping();

    bool InitComponent();
    int SendPing(std::string ip);
    // Interrupt handler
    void intHandler();
 private:
    unsigned short checksum(void *b, int len);
    char *dns_lookup(char *addr_host, struct sockaddr_in *addr_con);
    char* reverse_dns_lookup(char *ip_addr);
    void send_ping(int ping_sockfd, struct sockaddr_in *ping_addr, char *ping_dom, char *ping_ip, char *rev_host);
 private:
    // Define the Ping Loop
    int m_pingloop;
};

#endif
