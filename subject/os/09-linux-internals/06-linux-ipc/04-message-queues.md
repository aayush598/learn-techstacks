# Message Queues

## Overview
- Processes send/receive **structured messages** (typed, prioritized)
- Messages stored in kernel-managed queue
- Unlike pipes: **message boundaries** preserved, **priorities** supported

## POSIX Message Queues
```c
mqd_t mqd = mq_open("/my_queue", O_CREAT | O_RDWR, 0666, &attr);
mq_send(mqd, msg_ptr, msg_len, priority);
ssize_t n = mq_receive(mqd, buf, buf_size, &prio);
mq_close(mqd);
mq_unlink("/my_queue");
```
- `mq_open()`: create/open (returns descriptor)
- `mq_send()`: send message with priority (0 = lowest)
- `mq_receive()`: receive highest-priority message (FIFO within priority)
- `mq_notify()`: async notification (signal or thread) when message arrives
- Named: starts with `/`

## System V Message Queues
```c
int msqid = msgget(key, IPC_CREAT | 0666);
struct msgbuf { long mtype; char mtext[100]; };
msgsnd(msqid, &msg, len, 0);
msgrcv(msqid, &buf, len, mtype, 0);
msgctl(msqid, IPC_RMID, NULL);
```
- **mtype**: positive integer for selective receive
  - `msgrcv(..., 0, ...)` → any message
  - `msgrcv(..., 4, ...)` → first message with mtype=4
  - `msgrcv(..., -4, ...)` → first message with mtype ≤ 4
- Flags: `IPC_NOWAIT` (non-blocking), `MSG_EXCEPT`, `MSG_NOERROR`

## Attributes
| Parameter | POSIX | System V |
|-----------|-------|----------|
| Max messages | `mq_maxmsg` | `msg_qbytes` |
| Max message size | `mq_msgsize` | System limit |
| Priority | Per-message (unsigned int) | By mtype (long) |
| Notification | `mq_notify()` (signal/thread) | None |

## Comparison: Message Queues vs Pipes
| Feature | Message Queues | Pipes |
|---------|---------------|-------|
| Data model | Messages (typed, prioritized) | Byte stream |
| Boundaries | Yes | No |
| Priorities | Yes | No |
| Selective receive | Yes (by type) | No (all or nothing) |
| Max message size | Configurable | `PIPE_BUF` (4KB atomic) |

## Limits
- POSIX: `ulimit -q` (max queue size)
- System V: `kernel.msgmax`, `kernel.msgmnb`, `kernel.msgmni`
- View queues: `ipcs -q` (SysV), `ls /dev/mqueue/` (POSIX, if mounted)
