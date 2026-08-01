# Message Queues: POSIX vs System V

> **TL;DR**: Message queues pass **structured messages** (type + length + data) between processes, with priority and a kernel queue. **System V** (`msgget`/`msgsnd`/`msgrcv`, key-based, persistent) vs **POSIX** (`mq_open`/`mq_send`/`mq_receive`, name-based, `mq_*`) — the two API families, their kernel structures, and the trade-offs (ordering, priorities, portability, cleanup).

## 1. Why Does This Exist?
A pipe is a byte stream — if two processes want to exchange *records* ("task A, 40 bytes", "result B, 12 bytes"), they must frame them themselves. Message queues let the kernel do the framing: each message carries a type and length, the kernel stores it in a queue, and receivers pick messages by type. This adds structure (no manual framing), priorities (urgent messages jump the line), and a relaxed rendezvous (sender and receiver don't need to be active at the same moment — the queue buffers messages). The two standard API families grew from different design lineages: **System V** (keyed, kernel-persistent, `msgrcv` type-based selection) and **POSIX** (named, descriptor-based, with `mq_notify` and more predictable semantics).

## 2. How Does It Work?
**System V** (from SVR4):
- `msgget(key, flags)` → queue id (a `struct msqid_ds`); key can be `IPC_PRIVATE`, or derived from `ftok(path, id)`.
- `msgsnd(qid, msgbuf, size, flags)` — `struct msgbuf { long mtype; char mtext[]; }`; blocks if queue full unless `IPC_NOWAIT`.
- `msgrcv(qid, buf, size, type, flags)` — type selects: `type==0` → first msg; `type>0` → first msg of that exact type; `type<0` → first msg of lowest type ≤ |type| (priority ordering).
- Kernel `struct msg_queue` with linked list of messages, `msg_qbytes` limit, and per-queue wait queues.
- Persistence: the queue survives process exit; removed with `msgctl(IPC_RMID)` (or auto if `IPC_PRIVATE` creator dies... actually only via IPC_RMID or namespace teardown). Kernel limits: `msgmnb` (queue bytes), `msgmni` (queues), `msgmax` (per message).

**POSIX** (POSIX 1003.1b, since glibc 2.3.4):
- `mq_open("/name", O_CREAT, mode, attrs)` → `mqd_t` descriptor (an fd-like handle backed by `/dev/mqueue` or a pipefs-like mqueuefs). Names start with `/`.
- `mq_send`/`mq_timedsend`, `mq_receive`/`mq_timedreceive`, `mq_notify` (async notification), `mq_setattr` (priority), `mq_getattr`, `mq_unlink`.
- Each message has a `priority` (0..MQ_PRIO_MAX-1); `mq_receive` always returns the **highest-priority, then oldest** message (FIFO within priority). No arbitrary type-based selection like `msgrcv`.
- `mq_open` blocks if queue full (or `O_NONBLOCK`/timeouts). Signals/`mq_notify` give async wakeups.
- Kernel: `struct mqueue_inode_info` per queue; stored under `mqueuefs` (mounted at `/dev/mqueue`). Max messages/bytes via `MQ_OPEN_MAX`/`mq_maxmsg`.

## 3. When Is It Used?
- **Job/task distribution**: a producer enqueues jobs; N workers `msgrcv`/`mq_receive` with priority (urgent jobs jump).
- **Client–server**: requests and responses as typed messages (type = requester id) so one server can reply to many clients (`msgrcv(type=client_id)`).
- **Event buses**: publishing structured events with priorities in embedded/RTOS (VxWorks/SYS V heritage).
- **Legacy enterprise**: many classic Unix systems (Solaris, AIX) still ship System V; POSIX MQ is the modern replacement in glibc/Linux.
- **Decoupled producers/consumers**: the queue buffers when producer is faster or when consumer restarts.

## 4. Why Wasn't Another Approach Chosen?
- **Pipes (byte streams, no framing/priority)**: MQs add message boundaries + priority + type selection.
- **Shared memory (fast, but needs sync + no ordering)**: MQs give kernel-managed ordering and blocking — simpler to use correctly.
- **Sockets (network-capable, heavier)**: local MQs are cheaper than socket round trips for structured small messages; but sockets are more general (and `AF_UNIX` is often chosen today).
- **Signals (tiny payloads)**: MQs carry arbitrary-size payloads with priorities.
- **System V vs POSIX (chosen together)**: System V is keyed/persistent/type-selected; POSIX is name-based/descriptor-based/priority-ordered — Linux implements both for compatibility (glibc POSIX wrappers; `sysvipc` syscalls).

## 5. Intuition
**A post office with sorting trays**: senders drop letters (messages) into labeled trays. Each letter has a type (recipient) and a priority stamp. The post office (kernel) holds them until a recipient picks up. System V lets the recipient say "give me any letter" (type 0), "give me the letter for John" (exact type), or "give me the lowest-priority letter addressed to anyone in my group" (negative type = priority pick). POSIX is simpler: "give me the highest-priority letter, oldest first." If the tray is full, senders wait (or leave, `IPC_NOWAIT`/`O_NONBLOCK`).

## 6. Real-World Analogy
**A busy reception desk**: patients (messages) queue up. System V = the receptionist can call "next in line" (type 0), "next for Dr. Smith" (exact type), or "next non-urgent patient in any room" (priority pick). POSIX = a single line where **urgent patients always go first**, and among equal urgency it's first-come-first-served. If the waiting room is full, new patients wait outside (block) or leave (NOWAIT). The waiting room belongs to the clinic (kernel), not to any patient — it persists even when the person who made the appointment leaves.

## 7. Formal Definition
**System V**: `msgget(key_t key, int flags)` → `int msqid`. `msgsnd(int msqid, const void *msgp, size_t msgsz, int flags)`. `msgrcv(int msqid, void *msgp, size_t msgsz, long msgtyp, int flags)` — selection by `msgtyp` (0 / >0 / <0). Queue = `struct msg_queue { struct msg *q_messages; ... }` with limits `MSGMAX`, `MSGMNB`, `MSGQNI` (sysctl). Removed via `msgctl(msqid, IPC_RMID, ...)`.
**POSIX**: `mqd_t mq_open(const char *name, int oflag, mode_t mode, struct mq_attr *attr)`; `mq_send(mqd, const char *ptr, size_t len, unsigned prio)`; `mq_receive(mqd, char *ptr, size_t len, unsigned *priop)`. Messages sorted by `(priority desc, arrival asc)`. Limits via `struct mq_attr { mq_flags, mq_maxmsg, mq_msgsize, mq_curmsgs }`. Notification via `mq_notify(mqd, const struct sigevent *)`. Backed by `mqueuefs`; `/dev/mqueue` exposes queues for admin.

## 8. Example
System V — two processes exchange messages:
```c
// producer.c
struct msgbuf { long mtype; char mtext[256]; };
int qid = msgget(ftok("/tmp/keyfile", 65), IPC_CREAT | 0666);
struct msgbuf m = { .mtype = 1, .mtext = "task-1" };
msgsnd(qid, &m, 6, 0);   // 6 = strlen("task-1")
```
```c
// consumer.c — receive only type-1 messages
struct msgbuf m;
msgrcv(qid, &m, 256, 1, 0);   // type=1 → only type-1 messages
printf("got: %s\n", m.mtext);
```
Priority behavior (System V): a sender with `mtype=3` is *delivered before* a `mtype=2` only if the receiver asks for the lowest type (`msgtyp<0`). To make "higher type = more urgent", receiver uses `msgtyp = -max` ... the classic pattern: `msgrcv(qid, &m, size, -10, 0)` returns the lowest-type message of any type ≤ 10.

POSIX — a priority queue:
```c
mqd_t mq = mq_open("/jobs", O_CREAT | O_RDWR, 0600, &(struct mq_attr){.mq_maxmsg=10, .mq_msgsize=256});
mq_send(mq, "low", 3, 0);      // priority 0
mq_send(mq, "urgent", 6, 99);  // priority 99
unsigned prio; char buf[256];
mq_receive(mq, buf, 256, &prio);   // gets "urgent" (highest priority first)
```

## 9. Internal Working
1. **System V** `msgget` → `ipcget` (key→id lookup in `msg_ids`) → `newque` (alloc `struct msg_queue`, link into kernel IPC namespace).
2. `msgsnd` → `do_msgsnd` → check limits (`msgsz ≤ MSGMAX`, queue bytes ≤ MSGMNB) → copy message into a `struct msg_msg` (allocated via kmalloc/vmalloc if large) → link into the queue → wake waiting readers.
3. `msgrcv` → `do_msgrcv` → find message by `msgtyp` → copy to user → `free_msg` → wake blocked writers.
4. **POSIX** `mq_open` → `do_mq_open` in `ipc/mqueue.c` → `mqueue_get_inode` under `mqueuefs` → returns fd-like `mqd` → `fdget` ops → `mqueue_read_file`/`mqueue_write_file` implement `read`/`write` semantics.
5. `mq_send` → `do_mq_send` → insert into the priority-sorted list → wake waiters; if full and nonblocking → `EAGAIN`, else `schedule()` with `mq_waitq`.
6. `mq_notify` → registers a `sigevent` — the kernel sends `SIGEV_SIGNAL`/`SIGEV_THREAD`/`SIGEV_NONE` when a message arrives.
7. Both are namespaced per IPC namespace (containers isolate `msgget` keys and `/dev/mqueue`).

## 10. Time Complexity
- System V `msgsnd`/`msgrcv`: O(n) for the linked-list insert/remove (n = messages in queue) — worst O(n) because type selection scans; in practice small queues → O(1)-ish.
- POSIX `mq_send`/`mq_receive`: O(n) insert into priority list (sorted) — or O(n) worst for priority insertion; often O(1) for FIFO tail.
- Message copy: O(len) user↔kernel per message (unavoidable; this is the cost vs shared memory).
- Blocking: wait-queue O(1) enqueue/wakeup.
- `mq_notify` delivery: O(1) signal delivery via kernel.

## 11. Advantages
- **Structured messages**: type + length + data → no framing bugs.
- **Priorities**: urgent messages jump the queue (POSIX native; System V via `msgtyp<0`).
- **Decoupled senders/receivers**: kernel buffers messages; producer doesn't block on consumer speed.
- **Multi-consumer selection** (System V): `msgrcv` by type → a server can route replies by client id.
- **Persistent across process exit** (System V: until `IPC_RMID`; POSIX: until `mq_unlink`).
- **Portability**: both standardized; Linux glibc provides full POSIX API.

## 12. Disadvantages
- **Copy cost**: every message copied user→kernel→user (vs shared memory's zero copy).
- **Fixed limits**: queue depth/bytes are kernel-limited (`msgmnb`, `mq_maxmsg`) → backpressure is a policy, not a feature.
- **System V quirks**: key collisions, `ftok` hash collisions, no automatic cleanup (IPC_RMID can strand consumers), `msgrcv` type semantics are easy to get wrong.
- **Priority inversion potential**: a flood of high-priority messages starves low-priority ones (no fairness).
- **Same-host only** (no networking); sockets more general for distributed use.
- **API divergence**: System V vs POSIX are NOT interchangeable — a common interview trap and real portability issue.

## 13. Interview Questions
1. **Q: What is a message queue?** A: A kernel-managed queue of structured messages (type + length + data) that processes can send to and receive from — adding framing and priority over pipes.
2. **Q: System V vs POSIX message queues?** A: System V: `msgget/msgsnd/msgrcv`, key-based, persistent until `IPC_RMID`, type-based receive (`msgtyp`). POSIX: `mq_open/mq_send/mq_receive`, name-based (`/name`), priority-ordered receive (highest first), fd-like handles, `mq_notify` async notification.
3. **Q: How does `msgrcv` select messages?** A: `msgtyp==0` → first in queue; `msgtyp>0` → first with that exact type; `msgtyp<0` → first with the lowest type ≤ |msgtyp| (priority semantics).
4. **Q: What is `ftok`?** A: A function generating a System V key from a pathname + project id — used with `msgget`/`shmget`/`semget`; collisions are possible (poor design choice), hence `IPC_PRIVATE` for private queues.
5. **Q: What are the POSIX priority semantics?** A: `mq_receive` always returns the highest-priority message; among equal priorities, the oldest (FIFO). Priority range 0..`MQ_PRIO_MAX`-1.
6. **Q: When do send/receive block?** A: `msgsnd`/`mq_send` block when the queue is full (unless `IPC_NOWAIT`/`O_NONBLOCK`); `msgrcv`/`mq_receive` block when empty. Timeout variants: `mq_timedsend`/`mq_timedreceive`.
7. **Q: What is `mq_notify`?** A: POSIX async notification: register a `sigevent`; when a message arrives the kernel sends a signal or starts a thread — avoids blocking/polling.
8. **Q: What are the kernel limits?** A: System V: `MSGMAX` (max message), `MSGMNB` (max queue bytes), `MSGQNI` (max queues) — sysctls. POSIX: `mq_maxmsg`/`mq_msgsize` per queue at create; global `mqueue` limits.
9. **Q: How are System V IPC objects created and destroyed?** A: Created with `IPC_CREAT`; destroyed explicitly with `msgctl(IPC_RMID)`/`shmctl`/`semctl` — NOT automatically on process exit (persistence is a feature and a leak risk).
10. **Q: When would you use an MQ over a pipe?** A: When you need messages with priorities/types and decoupled producers/consumers (job queues, typed routing); pipes are simpler for plain byte streams.
11. **Q: When MQ over shared memory?** A: MQ when you want kernel-managed ordering/blocking and small structured messages; shared memory when throughput matters and you'll handle sync yourself.
12. **Q: Are MQs suitable for high-throughput?** A: Not for massive throughput — every message is copied twice (user→kernel→user). For bandwidth, use shared memory; for simplicity of structured exchange, MQs.

## 14. Follow-Up Questions
1. **Q: What's the difference between `mq_receive` and `read` on an MQ fd?** A: Functionally similar (POSIX MQ uses an fd-like handle), but `mq_receive` is message-aware (priority, length) — `read` on `/dev/mqueue` works but loses priority granularity.
2. **Q: What is `IPC_PRIVATE`?** A: A System V key that creates a new, private queue/segment/semaphore with a unique id — typically passed to children via fork (no `ftok` needed).
3. **Q: How do containers isolate message queues?** A: Each IPC namespace has its own key space and `/dev/mqueue` instance — processes in different namespaces can't see each other's queues.
4. **Q: What is priority inversion in MQs?** A: A stream of high-priority messages starves lower-priority ones — the receiver only ever sees high-priority traffic; need fairness or size limits (interplay with scheduler priority).

## 15. Coding Example
```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <string.h>
#include <unistd.h>

struct msgbuf { long mtype; char mtext[256]; };

int main(void) {
    key_t key = ftok("/tmp", 42);
    int qid = msgget(key, IPC_CREAT | 0666);
    if (qid == -1) { perror("msgget"); return 1; }

    pid_t pid = fork();
    if (pid == 0) {
        struct msgbuf m = { .mtype = 1 };
        strcpy(m.mtext, "worker result");
        msgsnd(qid, &m, strlen(m.mtext) + 1, 0);
        _exit(0);
    }
    struct msgbuf r;
    ssize_t n = msgrcv(qid, &r, sizeof r.mtext, 1, 0);  // type 1 only
    printf("parent got (type %ld): %s\n", r.mtype, r.mtext);
    msgctl(qid, IPC_RMID, NULL);                        // cleanup
    return 0;
}
```

## 16. Industry Usage
- **Linux kernel**: `ipc/msg.c` (System V), `ipc/mqueue.c` (POSIX), `include/uapi/linux/msg.h`, `mqueuefs`.
- **Legacy Unix enterprise** (Solaris/AIX/HP-UX): System V MQs still used in financial/telecom middleware.
- **glibc**: POSIX `mq_*` wrappers; `-lrt` historically required (`librt`).
- **Embedded/RTOS**: VxWorks/QNX message queues as the primary IPC (priority-ordered).
- **Containers**: IPC namespaces isolate `/dev/mqueue`; systemd uses socket activation + MQs in places.
- **Distributed systems**: modern stacks prefer `AF_UNIX` sockets or Redis/Kafka (network-capable) — MQs are the local-process cousin.

## 17. References
- `man 2 msgget`, `man 2 msgsnd`, `man 2 msgrcv`, `man 2 msgctl`, `man 3 ftok`.
- `man 3 mq_open`, `man 3 mq_send`, `man 3 mq_receive`, `man 3 mq_notify`, `man 3 mq_unlink`.
- Silberschatz, *Operating System Concepts*, Ch. 3.5.2 "Message Passing".
- Tanenbaum, *Modern Operating Systems*, Ch. 3.2.3 "Message passing".
- Linux kernel: `Documentation/sysctl/kernel.rst` (msg_* limits), `Documentation/userspace-api/sysvipc.rst`.
- Stevens, *UNIX Network Programming Vol 2* (Interprocess Communications).

## 18. Cheat Sheet
- System V: `msgget(key)` → `msgsnd`/`msgrcv`; key-based; `msgtyp` selection (0/+/−).
- POSIX: `mq_open("/name")` → `mq_send`/`mq_receive`; priority-ordered; `mq_notify`.
- Send blocks when full; receive blocks when empty (`NOWAIT`/`O_NONBLOCK`/timeout).
- Limits: `MSGMAX/MSGMNB/MSGQNI`; `mq_maxmsg/mq_msgsize`.
- System V persistent until `IPC_RMID`; POSIX until `mq_unlink`.
- Message = type + size + payload; two copies per transfer.
- Containers isolate via IPC namespaces.

## 19. Quiz
1. System V MQ creation call? a) mq_open b) msgget c) pipe d) shmget → **b**
2. POSIX MQ receive order? a) FIFO b) highest-priority-first c) type-selected d) random → **b**
3. `msgtyp > 0` returns? a) first b) exact type c) lowest type d) empty → **b**
4. Full-queue send default behavior? a) error b) blocks c) drops d) grows → **b**
5. System V cleanup? a) automatic b) `msgctl(IPC_RMID)` c) refcount d) `mq_unlink` → **b**
6. MQ's main cost vs shm? a) locking b) double copy c) memory d) signals → **b**

## 20. Flashcards
- **Q: System V MQ API?** → **A:** msgget/msgsnd/msgrcv, key-based.
- **Q: POSIX MQ API?** → **A:** mq_open/mq_send/mq_receive, priority order.
- **Q: msgtyp −1?** → **A:** lowest-type message ≤ |type| (priority pick).
- **Q: mq_notify?** → **A:** Async signal/thread on message arrival.
- **Q: When does send block?** → **A:** Queue full (or EAGAIN/nonblock).
- **Q: Main cost?** → **A:** User↔kernel copy per message.

## 21. Revision
Message queues give structured, prioritized, kernel-buffered exchange. System V is the classic: key-based `msgget`, `msgsnd`, `msgrcv` with type-based selection (0 = any, + = exact, − = priority pick), persistent until `IPC_RMID`. POSIX is the modern sibling: name-based `mq_open`, priority-ordered `mq_receive` (highest first), fd-like handles, `mq_notify` for async wakeups. Both block on full/empty queues with timeout/nonblocking escapes, both copy messages through the kernel (their cost vs shared memory), and both are per-namespace. Choose MQs for structured decoupled job/event exchange; prefer shared memory when throughput dominates and you'll handle sync yourself.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a message queue?" | 13 Q1 / 1 Why |
| "System V vs POSIX?" | 13 Q2 / 2 How |
| "How does msgrcv select?" | 13 Q3 / 2 How |
| "What is ftok?" | 13 Q4 / 2 How |
| "POSIX priority semantics?" | 13 Q5 / 7 Formal |
| "When does send/receive block?" | 13 Q6 / 9 Internal |
| "What is mq_notify?" | 13 Q7 / 2 How |
| "MQ vs pipe / vs shm?" | 13 Q10–11 / 4 Why not |
