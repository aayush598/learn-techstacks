# Process Hierarchies and ps Tree

> **TL;DR**: Processes form a tree rooted at PID 1 because every process is created by a parent via fork/clone — `ps`/`pstree` render that tree, and the parent-child structure drives reaping, signal delivery, cgroup placement, and container PID namespaces.

## 1. Why Does This Exist?
Because creation is always "parent creates child," the set of running processes is a tree (not a flat list) rooted at PID 1. The hierarchy exists because: (1) it defines *responsibility* — the parent must reap its children, (2) it defines *signal/session semantics* — kill(-pgid), SIGHUP cascades, (3) it provides a *management model* — systemd units, cgroups, and containers organize processes as trees, and (4) it's how operators *reason* about a system ("which process spawned that runaway?") via `ps`/`pstree`. Understanding the tree is how you debug process ancestry, zombie origins, and container leaks.

## 2. How Does It Work?
- `fork`/`clone` records `parent` (ppid) in the child's `task_struct`; `real_parent` tracks the true creator.
- The kernel keeps per-parent child lists (`children` list in `task_struct`) for `wait` (which child can I reap?) and reparenting.
- **PID 1** (systemd/init) is the root — adopted father of all orphans.
- `ps -ef`/`ps -eo pid,ppid,stat,comm` prints flat rows with PPID; `pstree -p` draws the tree; `/proc/<pid>/status` has PPID; `/proc/<pid>/task/` lists threads.
- **Thread groups**: threads of one process share the same TGID (the process's PID) — `ps` shows them as one row unless `-T`/`-L`.

## 3. When Is It Used?
- **Debugging ancestry**: find the parent of a runaway or orphan (`ps -o ppid`).
- **Service management**: systemd builds units; killing a unit's cgroup kills its whole process tree (clean teardown).
- **Signals**: `kill -TERM -<pgid>` broadcasts to a process group; session leaders control ttys.
- **Containers**: each container has its own PID namespace — inside it, PID 1 is the container init; the tree is namespace-scoped.
- **Monitoring**: `pstree`, `htop` tree view, `systemd-cgls` (cgroup tree).

## 4. Why Wasn't Another Approach Chosen?
- **Flat process list (no parent)**: loses responsibility/reaping semantics — who reaps whom? Signals become ambiguous. Rejected.
- **Multiple roots / no PID 1**: adoption and reaping break. PID 1's special role (can't be killed, orphan reaper) requires a single root.
- **Capability/object-based process identities (no ppid)**: modern systems add capabilities, but ppid-tree remains the model — it's simple and observable.
- **Hiding threads inside the process (no separate TID tree)**: Linux exposes threads as tasks (same tree, shared TGID) for scheduling/debugging; Windows hides thread detail by default. Both are valid; Linux's choice aids diagnostics.
- **No reparenting (child dies with parent)**: loses valid in-flight work; adoption is the chosen semantics.
The chosen model — ppid-based tree + adoption + per-namespace roots — is the POSIX standard and scales to containers.

## 5. Intuition
Processes are a **family tree / org chart**. The CEO (PID 1) spawned managers (systemd units), who hired staff (daemons), who each have interns (per-request children). When an employee quits, their reports are reassigned to the CEO's office (adoption by init). Reading the tree tells you who owns what and who's responsible for cleaning up — exactly like corporate accountability. Containers are like *franchise offices*: inside a franchise, the local manager (container init) is the "CEO," even though the real corporate CEO is above them.

## 6. Real-World Analogy
A **military command chain**: orders flow down the tree (signals), and accountability flows up (wait/reap). If a unit's commander is killed in action (parent dies), the soldiers are attached to the nearest higher command (reparented to init/subreaper). A deployed special-ops team (container) has its own local command (PID 1 in the namespace) but still reports up to the overall chain of command. `pstree` is the "organizational chart" view.

## 7. Formal Definition
A **process tree** is the parent-child structure induced by process creation: each process (except PID 1 and namespace-internal PIDs) has a parent (PPID) that created it via `fork`/`clone` and is responsible for reaping it; orphaned children are reparented to the nearest subreaper or PID 1. **PID namespace**: a view of the tree where PIDs are renumbered from 1 within the namespace, giving containers their own tree root. **Process group / session**: sets of related processes used for signal delivery (`kill(-pgid)`) and terminal control.

## 8. Example
```
$ pstree -p
systemd(1)─┬─sshd(800)───sshd(1200)───bash(1201)───grep(1234)
           ├─cron(650)
           └─docker(900)─┬─containerd-shim(1001)─┬─myapp(1010)───worker(1011)
                         └─ ...
```
Reading it: systemd is the root; sshd spawned a login shell (bash 1201) which ran grep (1234) — grep is bash's child. docker → containerd-shim → myapp → worker: the container's processes form a subtree (inside its PID namespace, myapp would be PID 1). A `ps -o pid,ppid,stat,comm` row set gives the same data flat.

## 9. Internal Working
1. **Creation links**: `copy_process` sets `child->parent = current`, `child->real_parent = current`; `add_child_to_parent` links into the parent's `children` list.
2. **PID allocation**: `alloc_pid` in a namespace → each namespace renumbers; the global tree has each PID once.
3. **Reparenting**: on parent exit, `forget_original_parent` walks the parent's children and reparents each to `find_new_reaper()` (nearest subreaper or PID 1); signals and `wait` now target the new parent.
4. **wait**: `do_wait` walks `children` (and grandchildren via `child_wait`/`ptrace`), finds a zombie, reaps.
5. **Grouping**: `setpgid`/`setsid` put processes in groups/sessions; `get_pid_task`, `find_task_by_vpid` resolve tree queries; `/proc` enumerates the tree (`fs/proc/base.c`).
6. **Namespaces**: `pid_ns` struct per namespace; `task_active_pid_ns` scopes lookups; container init is the namespace's PID 1.

## 10. Time Complexity
- `fork` + tree link: O(1) amortized.
- `wait` among N children: O(N) worst case to scan; O(1) typical (child finds itself).
- Reparenting on exit: O(children) per parent exit.
- `ps`/`pstree`: O(tasks) to enumerate; O(tasks × depth) for tree assembly.
- Namespace PID lookup: O(1) with per-ns idr map.

## 11. Advantages
- **Clear responsibility**: reaping, signals, and accounting map to the tree.
- **Debuggability**: `pstree`/`ps`/`ppid` instantly reveal ancestry (who spawned what).
- **Containment**: kill a subtree (`kill -pgid`, cgroup.kill, systemd Stop) cleanly tears down a group.
- **Namespace isolation**: each container gets a coherent, renumbered tree.
- **Simple model**: one root, adoption rules, well-defined semantics — easy to reason about.

## 12. Disadvantages
- **Tree traversal costs**: reparenting/reaping walk children lists; huge sibling lists (10k workers) make exit/wait slower.
- **Adoption surprises**: reparented processes' PPIDs change — monitoring that keys on ppid must handle it.
- **Zombie accumulation within subtrees** if an intermediate parent fails.
- **PID namespaces add confusion**: the same "PID 1" exists per container; global vs namespace PID mismatch in logs/tools.
- **Signals can be ambiguous**: `kill -pgid` vs `kill pid` vs per-namespace semantics trip operators.

## 13. Interview Questions
1. **Q: Why do processes form a tree?** A: Because every process is created by a parent (fork/clone); the only root is PID 1 (init/systemd) which adopts orphans. The tree defines reaping responsibility and signal/session semantics.
2. **Q: What does `ps -eo pid,ppid,stat,comm` show you?** A: Each process's PID, its parent (PPID), state, and command — the flat view of the tree. `pstree` renders the same data hierarchically.
3. **Q (TRICKY): Which process is PID 1 and why is it special?** A: `systemd`/init — the first user-space process, parent of all (via adoption), orphan reaper, cannot be killed (SIGKILL blocked by the kernel).
4. **Q: What is a PID namespace and how does it change the tree?** A: A namespace renumbers processes so each container sees itself starting at PID 1; the tree is namespace-scoped. `docker exec ps` shows container-local PIDs; the host sees global PIDs.
5. **Q: How do you find the parent of a runaway process?** A: `ps -o pid,ppid,comm -p <pid>` and read PPID; or `pstree -p -s <pid>` (show parents); then inspect that parent's logs/config. The ppid chain tells you who to fix/kill.
6. **Q (SCENARIO): An orphaned worker keeps running after its manager crashed. Who controls it now?** A: It's reparented to the nearest subreaper or PID 1 (systemd), which reaps it when it exits. You (root) can still kill it directly; its lifecycle is now init's responsibility.
7. **Q: What is a process group and session?** A: A process group is a set of processes sharing a PGID (created by setpgid); a session is a set of process groups (setsid). They gate signal delivery: `kill(-pgid)` signals the whole group; terminals deliver SIGHUP/SIGINT to the foreground group.
8. **Q: How does killing a systemd unit kill its whole tree?** A: systemd runs each unit in a cgroup and (on Stop) sends SIGTERM/SIGKILL to the cgroup — which contains the whole process subtree. That's cgroup-based tree containment.
9. **Q (PRODUCTION): `ps` shows 1000 worker processes with the same PPID. What's the architecture?** A: A pre-forking server (Apache/gunicorn/nginx workers) — the master (PPID) forked workers; the tree is shallow and wide. Killing the master may or may not kill workers (check daemon settings/cgroup).
10. **Q: How do threads appear in the process tree?** A: All threads of a process share the same TGID (the process's PID); `ps` shows one row; `ps -T`/`-L` or `/proc/<pid>/task/` lists threads as separate tasks with distinct TIDs.
11. **Q: What is `PR_SET_CHILD_SUBREAPER` and why do container runtimes use it?** A: It marks a process to adopt orphaned *descendants* before PID 1 — containerd uses it so container child processes are reaped by the runtime, not the host init.
12. **Q (TRICKY): In a container, why does `ps` inside see different PIDs than `ps` on the host?** A: PID namespaces renumber PIDs per namespace. Inside the container, its init is PID 1; on the host, the same task has its global PID. `getpid()` returns the namespace-scoped PID.
13. **Q: How does the kernel keep the children list and why does exit walk it?** A: `task_struct` has `children`/`sibling` lists; on exit, `forget_original_parent` iterates them to reparent children — the cost is O(children), which is why pathological wide trees slow exit.
14. **Q: What is the relationship between `ppid` in `/proc` and `getppid()`?** A: Both read the PCB's `real_parent`/`parent` fields; `/proc/<pid>/status`'s PPid line and the `getppid()` syscall return the same value (they differ subtly for traced/thread processes).
15. **Q: How do you display the full ancestry of a process?** A: `pstree -ps <pid>` walks up the tree; `ps -o pid,ppid,comm --ppid <pid>` lists children; combine them to map the subtree. `/proc/<pid>/task/<tid>/children` lists kernel-visible children.

## 14. Follow-Up Questions
1. **Q: What is the difference between `parent` and `real_parent` in task_struct?** A: `real_parent` = actual creator; `parent` = current reaping parent (can differ when a debugger attaches via ptrace). wait() uses the effective parent.
2. **Q: What does SIGHUP do in a tree context?** A: When the session leader's tty closes, SIGHUP goes to the foreground process group — the classic "SSH logout kills my background job" behavior (unless nohup/setsid).
3. **Q: How does a "double-fork" change the tree?** A: The grandchild's parent (the intermediate fork) exits, so the grandchild is reparented to init — it's no longer in the original session's subtree and can't be waited by the original parent.
4. **Q: What is a "process tree kill" and how do you do it safely?** A: Kill the group (kill -TERM -pgid) or use systemd Stop / cgroup.kill; safer than killing PIDs individually because it handles the whole subtree at once.
5. **Q: Why does `pstree` sometimes show `─+=` markers?** A: pstree draws box-drawing characters for depth; `=`/`+` indicate the tree structure. The exact glyphs are cosmetic — the tree is the data.

## 15. Coding Example
```c
/* Walk the process tree by reading /proc/<pid>/status PPID */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void print_ancestors(int pid) {
    for (int cur = pid; cur > 0 && cur != 1; ) {
        char path[64], line[256];
        snprintf(path, sizeof path, "/proc/%d/status", cur);
        FILE *f = fopen(path, "r");
        if (!f) { printf(" %d (gone)\n", cur); break; }
        int ppid = -1;
        while (fgets(line, sizeof line, f))
            if (strncmp(line, "PPid:", 5) == 0) { ppid = atoi(line + 5); break; }
        fclose(f);
        printf("%d", cur);
        cur = ppid;
        if (cur > 0) printf(" -> ");
    }
    printf("\n");
}

int main(int argc, char **argv) {
    print_ancestors(atoi(argv[1]));
    return 0;
}
```
```bash
# Tree inspection commands
pstree -p | head -30
ps -eo pid,ppid,stat,comm --sort=ppid | head -20
ps -ef --forest | head -25
# children of a specific PID
ps --ppid 1 -o pid,comm
# full ancestry of a PID
pstree -ps $(pgrep -n sleep)
```

## 16. Industry Usage
- **Linux**: `kernel/fork.c` (child linking), `kernel/exit.c` (reparenting), `fs/proc/base.c` (`/proc/<pid>/task/<tid>/children`, status), `kernel/pid.c`, `kernel/nsproxy.c` (namespaces).
- **systemd**: units organized as trees in cgroups; `systemctl status` shows the tree; `systemd-cgls` shows cgroup hierarchy.
- **Containers**: runc/containerd create PID namespaces + subreaper; Kubernetes "PID 1 zombie problem" is a tree/reaping issue solved by init-in-pod (tini) or subreaper.
- **Orchestrators**: Kubernetes PID limits per pod (cgroup pids.max) protect the tree from fork bombs.
- **Monitoring**: Prometheus `node_exporter`, `pstree`, `htop` tree mode — all read the process tree.
- **Interview angle**: tree/ppid questions appear as practical debugging and container-architecture questions at FAANG.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 3.2-3.3 (Process Scheduling/Tree).
- Linux man: `ps(1)`, `pstree(1)`, `pid_namespaces(7)`, `credentials(7)`.
- Linux source: `kernel/pid.c`, `kernel/pid_namespace.c`, `kernel/exit.c`, `include/linux/pid.h`.
- Kerrisk, *The Linux Programming Interface* (processes & namespaces).
- Docker/Kubernetes docs on PID namespace and init processes.

## 18. Cheat Sheet
- Processes form a tree rooted at PID 1 (systemd).
- `ps -o pid,ppid` / `pstree -p` render the tree.
- PID 1 = orphan reaper; can't be killed.
- Orphans reparent to nearest subreaper or init.
- Process groups (setpgid) + sessions (setsid) gate signals.
- `kill -TERM -pgid` = tree kill; systemd Stop = cgroup kill.
- Threads: same TGID, distinct TID; ps -T/-L shows them.
- PID namespaces renumber; container init = namespace PID 1.
- containerd uses PR_SET_CHILD_SUBREAPER.
- Container "PID 1 zombie problem" → run tini / subreaper.

## 19. Quiz
1. The root of the process tree is: a) kthreadd b) PID 1/systemd c) the shell d) PID 2 → **b**
2. `ps -o pid,ppid,comm` shows: a) thread TIDs b) parent relationships c) kernel modules d) cgroups → **b**
3. Orphaned processes are adopted by: a) the shell b) PID 1/subreaper c) the kernel d) kthreadd → **b**
4. `kill -TERM -<pgid>` signals: a) one pid b) a process group c) a cgroup d) all users → **b**
5. A process's threads share: a) TID b) TGID (the PID) c) PPID only d) nothing → **b**
6. Inside a PID namespace, container init is: a) global PID 1 b) namespace PID 1 c) PID 0 d) kthreadd → **b**
7. containerd reaps container orphans via: a) setsid b) PR_SET_CHILD_SUBREAPER c) PID 1 d) PDEATHSIG → **b**
8. `pstree -ps <pid>` shows: a) children b) ancestors c) threads d) sockets → **b**
9. When a parent exits, its children are: a) killed b) reparented c) zombied d) orphaned forever → **b**
10. systemd kills a unit's tree by: a) kill -pgid only b) cgroup-based kill c) PID 1 suicide d) nothing → **b**

## 20. Flashcards
- **Q: Process tree root?** → **A:** PID 1 (systemd/init).
- **Q: How to see the tree?** → **A:** pstree -p, ps -o pid,ppid, ps --forest.
- **Q: Who adopts orphans?** → **A:** Nearest subreaper or PID 1.
- **Q: kill -TERM -pgid?** → **A:** Signal the whole process group.
- **Q: Threads in the tree?** → **A:** Same TGID, distinct TID; ps -T/-L.
- **Q: PID namespaces?** → **A:** Renumber PIDs; container init = PID 1 inside.
- **Q: subreaper use?** → **A:** containerd reaps container orphans.
- **Q: Why PID 1 special?** → **A:** Orphan reaper; unkillable.
- **Q: Container zombie problem?** → **A:** No reaping init inside → run tini/subreaper.

## 21. Revision
Every process is created by a parent, so processes form a tree rooted at PID 1 (systemd). The tree defines reaping responsibility, signal delivery (process groups/sessions), and containment (systemd cgroups, kill -pgid). `ps -o pid,ppid` and `pstree` render it; orphans reparent to the nearest subreaper or init; threads share TGID but have distinct TIDs; PID namespaces renumber the tree per container so container init is PID 1 inside. Debugging runaway or orphaned processes is tree reading.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why do processes form a tree?" | 13 Q1 / 1 Why Does This Exist |
| "What is PID 1's role?" | 13 Q3 / 9 Internal Working |
| "Find a runaway process's parent" | 13 Q5 / 16 Industry Usage |
| "What is a PID namespace?" | 13 Q4 / 2 How It Works |
| "How to kill a whole tree?" | 13 Q8 / 6 Analogy |
| "Orphaned workers — who controls them?" | 13 Q6 / 9 Internal Working |
| "Process groups & sessions?" | 13 Q7 / 7 Formal Definition |
| "Threads in the tree?" | 13 Q10 / 2 How It Works |
| "Container PID 1 zombie problem?" | 13 Q11-12 / 16 Industry Usage |
| "How does the kernel reparent?" | 13 Q13 / 9 Internal Working |
