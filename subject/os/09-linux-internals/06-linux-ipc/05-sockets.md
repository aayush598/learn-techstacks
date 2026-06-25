# Sockets

## Socket Types
| Domain | Purpose | Address format |
|--------|---------|----------------|
| **AF_UNIX** (AF_LOCAL) | Local IPC, same host | Pathname (`/tmp/sock`) |
| **AF_INET** | IPv4 over network | IP:port (e.g., `192.168.1.1:80`) |
| **AF_INET6** | IPv6 | IPv6 address:port |
| **AF_NETLINK** | Kernel↔user communication | Netlink socket |

## Socket Sockets
| Type | Description |
|------|-------------|
| **SOCK_STREAM** | TCP (reliable, in-order, connection-oriented) |
| **SOCK_DGRAM** | UDP (unreliable, datagrams, connectionless) |
| **SOCK_RAW** | Direct IP packets (requires root) |
| **SOCK_SEQPACKET** | Reliable, message boundaries (Unix domain) |

## Socket API (server)
```c
int sfd = socket(AF_INET, SOCK_STREAM, 0);
bind(sfd, (struct sockaddr *)&addr, sizeof(addr));
listen(sfd, backlog);      // backlog = pending queue size
int cfd = accept(sfd, NULL, NULL);
read(cfd, buf, size);
write(cfd, response, len);
close(cfd);
```

## Socket API (client)
```c
int sfd = socket(AF_INET, SOCK_STREAM, 0);
connect(sfd, (struct sockaddr *)&addr, sizeof(addr));
write(sfd, request, len);
read(sfd, buf, size);
close(sfd);
```

## send() / recv() vs write() / read()
- `send()` / `recv()`: socket-specific flags (`MSG_OOB`, `MSG_PEEK`, `MSG_NOSIGNAL`)
- `write()` / `read()`: generic, works on any fd (including sockets)
- For datagram sockets, use `sendto()` / `recvfrom()` (specify peer address)

## Unix Domain Sockets
- **Faster than AF_INET loopback** (no TCP/IP overhead, kernel copies only)
- Stream or datagram (both reliable within same host)
- `socket(AF_UNIX, SOCK_STREAM, 0)`
- Bind to path in filesystem (use `unlink()` before bind to clean stale)

## I/O Models
| Model | Blocking | Thread per conn | Scalability |
|-------|----------|----------------|-------------|
| **Blocking** | Yes | 1 thread/conn | Poor |
| **select()** | Monitor up to FD_SETSIZE (1024) | 1 thread | Limited |
| **poll()** | No max limit, O(n) scan | 1 thread | Moderate |
| **epoll()** | O(1), edge/level-triggered, millions of fds | 1 thread | **Best** |

## epoll
```c
int epfd = epoll_create1(0);
struct epoll_event ev = {.events = EPOLLIN, .data.fd = sfd};
epoll_ctl(epfd, EPOLL_CTL_ADD, sfd, &ev);
int nfds = epoll_wait(epfd, events, MAX_EVENTS, -1);
```
- **Level-triggered** (default): event fires while data available
- **Edge-triggered** (EPOLLET): event fires only once on state change
- Used in **nginx**, **node.js**, **Redis** for high concurrency
