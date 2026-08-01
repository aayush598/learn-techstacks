# Zombie, Orphan, and Daemon Processes

> **TL;DR**: Zombies are dead-but-unreaped processes (PCB kept until `wait`), orphans are children whose parent died (adopted by PID 1), and daemons are long-lived background processes that deliberately detach from the terminal — three "afterlife" states every production system must manage correctly.

## 1. Why Does This Exist?
Processes die but their exit *status* must be delivered to the parent, and the parent may be busy — so the kernel retains the exit record. Zombies exist to guarantee the parent can always `wait()` and learn *how* the child died (exit code, signal). Orphans exist because parents can crash before their children finish — the kernel must not lose the process, so PID 1 adopts it. Daemons exist because background services (web, SSH, monitoring) must survive the terminal session that started them — they detach so their lifetime is the machine's, not the terminal's. Together these three define the process "afterlife" — what happens after (or without) a clean parent-child handshake.

## 2. How Does It Work?
- **Zombie (state Z)**: child calls `exit()` → resources freed (memory, files), but the PCB (task_struct) and exit status remain, state = `EXIT_ZOMBIE`, SIGCHLD sent to parent. Parent's `wait()`/`waitpid()` reaps it → `release_task` frees the PCB.
- **Orphan**: parent dies before the child → the child is reparented to **PID 1** (systemd/init), which must reap it (systemd reaps via subreaper-style handling). If PID 1 doesn't reap, orphans become permanent zombies.
- **Daemon**: a process that (1) `fork`s, parent `_exit`s (so the daemon is reparented to init), (2) `setsid()` (new session, no controlling tty), (3) `chdir("/")`, `umask(0)`, (4) redirects stdin/stdout/stderr to `/dev/null` (or a log), (5) optionally double-forks to avoid re-acquiring a tty. systemd manages daemons as services today (no manual daemonization needed).

## 3. When Is It Used?
- **Zombies**: appear in `ps` as `Z`; commonly during `fork`-happy workloads when a parent crashes before `wait`; `init` should reap orphans. Watch for zombie *piles* = parent bug.
- **Orphans**: after a parent crash; `systemd` (PID 1) reaps them; `subreaper` (prctl `PR_SET_CHILD_SUBREAPER`) lets intermediate managers adopt orphaned children (e.g., Docker's containerd).
- **Daemons**: system services (sshd, cron, journald), app background workers, custom services via systemd units; also "daemon mode" flags (`-d`).
- **Reaping**: `wait`, `waitpid`, `waitid`, `SIGCHLD` handlers, `signal(SIGCHLD, SIG_IGN)` (auto-reap), `SA_NOCLDWAIT`.

## 4. Why Wasn't Another Approach Chosen?
- **Free the PCB immediately at exit (no zombie)**: then the parent could never learn the exit status — Unix guarantees the status must be collectable. Alternative: kernel always sends the status via a channel (Linux has pidfd + `pidfd_send_signal`/`waitid(P_PIDFD)`), but the classic contract keeps the PCB. Rejected for status-loss.
- **No reaping requirement (status stored elsewhere)**: keeping it in the parent's table costs memory; the zombie model (tiny PCB) is the pragmatic guarantee.
- **No adoption (orphan dies)**: wasteful and surprising — orphans are usually valid work (the parent just crashed). Adoption by init preserves the process.
- **Daemons as kernel threads**: some services are kernel threads (ksoftirqd), but most must be user space (safe, crashable, restartable) — hence user daemons.
- **No daemonization (services die with terminal)**: historically services needed detachment; modern `systemd` runs services without daemonization (the service manager is the parent). Both exist.
The chosen model — zombies (status guarantee), adoption (no lost children), daemonization (survival) — is the POSIX contract.

## 5. Intuition
A zombie is like a **terminated employee still on the payroll sheet** until HR (the parent) files the paperwork (`wait`). An orphan is a **child whose parents died in a crash** — social services (PID 1) takes over custody. A daemon is like a **24/7 security guard who lives at the office**: they have no personal life (terminal), report to the company owner (init), and never clock out (no tty). Guards in modern managed buildings are hired via the facility manager (systemd) rather than setting up their own lodgings.

## 6. Real-World Analogy
A **hospital discharge process**: the patient (child) is medically done (exit) but the discharge paperwork (exit status) must be signed by the attending doctor (parent's wait). If the doctor leaves (parent dies), the hospital admin (init) signs. If the admin also fails to sign, the discharged patient "lingers on the floor" (permanent zombie). A home-care nurse (daemon) who's on 24/7 call and lives near the patient is a background process that detached from any clinic shift (terminal).

## 7. Formal Definition
- **Zombie process**: a process that has called `exit()` and released all resources but whose `task_struct` and exit status are retained because the parent has not yet called `wait()/waitpid()`; state `EXIT_ZOMBIE` (`Z`).
- **Orphan process**: a process whose parent has terminated; it is reparented to the subreaper (PID 1, systemd, or a `PR_SET_CHILD_SUBREAPER` process) which is responsible for reaping it.
- **Daemon process**: a long-lived background process running in its own session without a controlling terminal (created via `fork`+`setsid`+redirection, or managed as a systemd service), typically started at boot.

## 8. Example
```
$ bash -c 'sleep 5 & sleep 100' &
$ sleep 0.3; ps -eo pid,ppid,stat,comm | grep -E "sleep|bash"
  3000 1     S  bash        (our subshell; reparented to init after its parent exits)
  3001 3000  S  sleep 5
  3002 3000  S  sleep 100
# wait for the 5s sleep to die:
$ sleep 5; ps -eo pid,ppid,stat,comm | grep 3001
  3001 3000  Z  sleep     <- zombie (parent 3000 hasn't waited)
# parent's bash exits -> 3002 reparented to init (orphan); init will reap it
```
Key observations: `Z` state = zombie; PPID becoming `1` = orphan/adoption.

## 9. Internal Working
1. **exit()**: `do_exit` → `exit_signals`, `exit_mm` (free pages), `exit_files`, `exit_fs`; sets `exit_state = EXIT_ZOMBIE`; sends `SIGCHLD` to the parent; parent notified via `wake_up_parent`.
2. **wait()**: `wait4`/`waitid` → `do_wait` → finds the child, reads `exit_code`, calls `release_task` → `__put_task_struct` frees PCB; PID freed.
3. **Orphan handling**: on parent exit, `exit_notify` → `forget_original_parent` → each child is reparented to the nearest subreaper (or PID 1); the new parent must reap them.
4. **Daemonization**: `daemon(nochdir, noclose)` or manual: `fork()`; parent `_exit()`; `setsid()`; (optionally fork again); `chdir("/")`; `umask(0)`; `dup2(/dev/null, 0/1/2)`; then the daemon loops serving.
5. **systemd services**: `Type=simple` services are exec'd directly by systemd (PID 1) — no daemonization; `Type=forking` handles legacy daemons by watching for the forked PID.

## 10. Time Complexity
- Zombie lifetime: O(1) — until the parent waits.
- `wait`/`waitpid`: O(children) worst case to find the right child; O(1) common.
- Reparenting on parent exit: O(children) per exit.
- Reaping by init: O(1) per orphan.
- Daemon fork+setsid: O(1) + process-creation cost.

## 11. Advantages
- **Guaranteed exit-status delivery** (zombie contract) — no lost information.
- **No lost work on parent crash** (adoption) — orphaned children continue and are cleaned up.
- **Survivable background services** (daemons) — the machine's uptime, not the terminal's.
- **Observable**: `ps` shows Z/S/T states; `systemctl status` shows service state.

## 12. Disadvantages
- **Zombie piles leak PIDs/PCBs**: if a parent never waits, each zombie holds a PID and a few KB of kernel memory; thousands of zombies exhaust `pid_max`/process limits.
- **Init must be reliable**: if PID 1 is buggy or slow, orphans accumulate as zombies (the classic "systemd doesn't reap" incidents).
- **Daemonization is fiddly**: manual daemons have startup-order races, double-fork subtleties, and tty-reacquire bugs; systemd `Type=simple` sidesteps it.
- **Zombies can't be killed**: `kill -9` on a zombie is a no-op (it's already dead) — only the parent's `wait` can reap it; users often panic over "unkillable zombies."

## 13. Interview Questions
1. **Q: What is a zombie process?** A: A process that has exited but whose PCB (and exit status) is retained because the parent hasn't called `wait()`. State Z; holds a PID + PCB; can't be killed.
2. **Q: What is an orphan process?** A: A process whose parent died; it's reparented to PID 1 (init/systemd) or the nearest subreaper, which must reap it.
3. **Q: How do you prevent zombies?** A: Have the parent `wait()`/`waitpid()` each child (or handle SIGCHLD), install `signal(SIGCHLD, SIG_IGN)` or `SA_NOCLDWAIT` for auto-reap, or rely on the parent being short-lived. A zombie can't be killed — only reaped.
4. **Q (TRICKY): Can you `kill -9` a zombie?** A: No — it's already dead (exit completed); the signal is a no-op. The only fix is making the parent `wait()` — or the zombie being reparented to a reaper (init) that reaps it.
5. **Q (PRODUCTION): You see 10,000 zombies. What's the cause and fix?** A: A parent that doesn't wait (bug) or a stuck parent. Zombies are harmless individually but exhaust PIDs/PCBs. Fix the parent (add wait/SIGCHLD handler) or restart it; check `ppid` to find the culprit.
6. **Q: What does a daemon do at startup?** A: `fork` (parent exits), `setsid` (new session, detach from controlling tty), optionally double-fork, `chdir("/")`, `umask(0)`, redirect stdin/stdout/stderr to /dev/null or logs. Modern daemons are run by systemd instead.
7. **Q: What is `setsid` for?** A: Creates a new session with the calling process as leader and no controlling terminal — the crucial step that lets a process outlive and ignore the terminal that started it.
8. **Q: Why do daemons double-fork?** A: So the daemon is reparented to init (after the first fork's parent exits) and, after a second fork, it's *not* a session leader — preventing it from reacquiring a controlling tty if it opens a terminal device.
9. **Q (SCENARIO): A service dies when you close the SSH session. What's wrong?** A: It wasn't daemonized (still has the controlling tty / SIGHUP on session end). Fix: run it under systemd, `nohup`/`setsid`, or daemonize properly.
10. **Q: How does systemd avoid daemonization?** A: systemd is PID 1 and keeps the service as its child (`Type=simple`); no fork/setsid needed — systemd manages lifetime, and the service's stdout goes to journald.
11. **Q: What is a subreaper?** A: A process that declared `prctl(PR_SET_CHILD_SUBREAPER)` and adopts orphaned descendants instead of PID 1 — e.g., containerd/Docker so containers' orphans are reaped by the container runtime.
12. **Q (TRICKY): If PID 1 is a zombie, what happens?** A: PID 1 can't be killed (kernel blocks SIGKILL on it) and its reaping duty is critical; a buggy init that doesn't reap orphans → orphan zombies accumulate. Modern systemd is robust here.
13. **Q: What's the difference between `wait`, `waitpid`, and `waitid`?** A: `wait` (any child), `waitpid(pid, ...)` (specific child or WNOHANG nonblocking), `waitid` (richer: P_PID/P_PIDFD, events). All reap and return exit status.
14. **Q: How does SIGCHLD relate to reaping?** A: The kernel sends SIGCHLD when a child stops/exits; a handler that calls waitpid reaps promptly; `SIG_IGN` or `SA_NOCLDWAIT` causes automatic reaping (no zombie).
15. **Q (PRODUCTION): What is `systemd`'s `Type=forking` and `PIDFile`?** A: For legacy daemons that fork themselves, systemd waits for the daemon to signal readiness (the parent forks and the original exits), then tracks the forked PID via `PIDFile` — allowing the old daemon model to run under the new manager.

## 14. Follow-Up Questions
1. **Q: Can a process be both zombie and daemon?** A: No — a daemon is a *running* background process; a zombie is dead-unreaped. Daemons that exit without being reaped (e.g., a forked child of a daemon) can become zombies.
2. **Q: What does `nohup` do?** A: Ignores SIGHUP so the process survives the terminal closing — a poor-man's daemonization (doesn't setsid, so it may still have a tty).
3. **Q: What is the difference between a zombie and a dead-but-hold-on-wait process?** A: Same thing — "zombie" is the observable state; the kernel keeps the PCB until wait. No semantic difference.
4. **Q: Why does `ps` show PID 1 as `sshd`'s parent after `setsid`?** A: When the daemon's forked child reparents to init, `ps` reports ppid=1 — a reliable way to detect daemonized processes.
5. **Q: What is `PR_SET_PDEATHSIG`?** A: A prctl setting a signal delivered when the *parent* dies — the reverse of adoption: the child wants to die with its parent (useful for per-request worker hierarchies).

## 15. Coding Example
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/wait.h>
#include <fcntl.h>

/* 1) Daemonize: detach from terminal, survive sessions */
void daemonize(void) {
    pid_t pid = fork();
    if (pid < 0) exit(1);
    if (pid > 0) _exit(0);          /* parent exits */
    setsid();                        /* new session, no controlling tty */
    pid = fork();                    /* second fork: not a session leader */
    if (pid < 0) exit(1);
    if (pid > 0) _exit(0);
    chdir("/");
    umask(0);
    int devnull = open("/dev/null", O_RDWR);
    dup2(devnull, 0); dup2(devnull, 1); dup2(devnull, 2);
}

/* 2) Reap children: reap on SIGCHLD so no zombies pile up */
void on_sigchld(int sig) {
    int status;
    while (waitpid(-1, &status, WNOHANG) > 0) /* reap until none */
        ;
}
int main(void) {
    struct sigaction sa = { .sa_handler = on_sigchld };
    sigaction(SIGCHLD, &sa, NULL);

    if (fork() == 0) { sleep(1); _exit(0); }   /* child; exits -> SIGCHLD */
    sleep(3);                                   /* handler reaps it */
    printf("no zombies here\n");
    return 0;
}
```
```bash
# See zombies/orphans in action
( sleep 30 & )          # child of the subshell; subshell exits -> orphan adopted by init
sleep 0.2
ps -eo pid,ppid,stat,comm | grep sleep     # ppid will be 1 (orphan, adopted by init)
kill %1 2>/dev/null
```

## 16. Industry Usage
- **Linux**: `kernel/exit.c` (`do_exit`, `release_task`, reparenting via `forget_original_parent`), `kernel/fork.c` (SIGCHLD), `kernel/sys.c` (setsid), `kernel/prctl.c` (subreaper, PDEATHSIG).
- **Production**: systemd (PID 1) reaps orphans; containerd uses `PR_SET_CHILD_SUBREAPER` for container processes; SREs diagnose "zombie floods" and "orphaned processes."
- **Cloud/containers**: Docker uses containerd-shim (reaper) per container; Kubernetes kubelet's PID-1-in-pod ensures init reaps container zombies — the famous "PID 1 zombie problem in containers."
- **Daemons**: sshd, cron, journald, agent daemons (datadog, node_exporter); run under systemd with journald logging.
- **Interview angle**: zombies/orphans/daemons are among the most asked "practical Linux" questions — every backend/SRE interview includes one.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 3.3 (Process Termination).
- Tanenbaum, *Modern OS*, Ch. 2.1.5.
- Linux man: `wait(2)`, `fork(2)`, `setsid(2)`, `daemon(3)`, `prctl(2)` (PR_SET_CHILD_SUBREAPER, PR_SET_PDEATHSIG), `systemd.service(5)`.
- Linux source: `kernel/exit.c`, `kernel/sys.c` (setsid).
- Kerrisk, *The Linux Programming Interface* (Process termination/daemons).

## 18. Cheat Sheet
- Zombie = exited + unreaped (state Z); PCB/PID retained; unkillable; needs wait().
- Orphan = parent died; adopted by init/subreaper; must be reaped.
- SIGCHLD handler + waitpid(WNOHANG) loop = robust reaping.
- `signal(SIGCHLD, SIG_IGN)` = auto-reap.
- Daemonize: fork → parent exit → setsid → (double fork) → chdir("/") → umask → redirect fds.
- subreaper (containerd) = adopt & reap container orphans.
- PID 1 can't be killed; its job includes reaping.
- `PR_SET_PDEATHSIG` = die with parent.
- systemd `Type=simple` avoids daemonization; `Type=forking` supports legacy.
- Zombie piles exhaust PIDs → monitor and fix parents.

## 19. Quiz
1. A zombie is: a) stopped b) exited, unreaped c) orphaned d) running → **b**
2. You can kill a zombie with: a) kill -9 b) SIGTERM c) only wait() d) reboot → **c**
3. An orphan is adopted by: a) the kernel b) PID 1 / subreaper c) the shell d) nobody → **b**
4. `setsid()` detaches a process from: a) its parent b) the controlling terminal c) init d) cgroups → **b**
5. Which reaps children non-blockingly? a) wait b) waitpid(WNOHANG) c) sleep d) kill → **b**
6. containerd uses which to adopt orphans? a) setsid b) PR_SET_CHILD_SUBREAPER c) PDEATHSIG d) double fork → **b**
7. A daemon must NOT have: a) a PID b) a controlling terminal c) init as parent d) a log → **b**
8. `nohup` protects against: a) SIGTERM b) SIGHUP c) SIGKILL d) SIGSEGV → **b**
9. `PR_SET_PDEATHSIG` means: a) die with parent b) adopt orphans c) survive parent d) re-parent → **a**
10. systemd `Type=simple` services: a) daemonize themselves b) are run directly as PID 1's children → **b**

## 20. Flashcards
- **Q: Zombie?** → **A:** Exited, unreaped; PCB+status kept; needs wait().
- **Q: Orphan?** → **A:** Parent died; adopted by init/subreaper.
- **Q: How to auto-reap?** → **A:** SIG_IGN/SIGCHLD handler with waitpid loop.
- **Q: Daemonize steps?** → **A:** fork, setsid, double-fork, chdir, umask, redirect fds.
- **Q: Why double fork?** → **A:** Not a session leader → can't reacquire tty.
- **Q: Subreaper?** → **A:** process adopting orphans (containerd) via prctl.
- **Q: Can PID 1 be killed?** → **A:** No; it must reap orphans.
- **Q: PDEATHSIG?** → **A:** Signal delivered when parent dies.

## 21. Revision
Zombies are exited-but-unreaped processes holding a PCB/PID until the parent waits; they can't be killed, only reaped — handle via waitpid loops or SIG_IGN. Orphans are children of dead parents, adopted by PID 1 or a subreaper (containerd) which reaps them. Daemons detach with fork+setsid(+double fork)+chdir+umask+fd redirection, or are run directly by systemd. The container "PID 1 zombie problem" is this model in production. Reaping, adoption, and detachment are the three process-lifecycle contracts every system must honor.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a zombie/orphan?" | 7 Formal Definition / 8 Example |
| "Can you kill a zombie?" | 13 Q4 / 12 Disadvantages |
| "10,000 zombies in prod?" | 13 Q5 / 16 Industry Usage |
| "How to daemonize?" | 13 Q6 / 9 Internal Working |
| "What does setsid do?" | 13 Q7 / 2 How It Works |
| "Why double-fork?" | 13 Q8 / 4 Why Not |
| "Service dies on SSH logout?" | 13 Q9 / 16 Industry Usage |
| "How does systemd run services?" | 13 Q10, Q15 / 2 How It Works |
| "What is a subreaper?" | 13 Q11 / 16 Industry Usage |
| "SIGCHLD + reaping?" | 13 Q14 / 9 Internal Working |
