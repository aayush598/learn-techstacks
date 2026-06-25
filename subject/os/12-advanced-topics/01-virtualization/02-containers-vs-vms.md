# Containers vs Virtual Machines

## Comparison Table

| Property | Container | Virtual Machine |
|----------|-----------|-----------------|
| **Kernel** | Shares host kernel (same OS) | Full guest OS (independent kernel) |
| **Startup** | Milliseconds | Seconds to minutes |
| **Size** | MBs (just app + deps) | GBs (full OS image) |
| **Isolation** | Weak (namespaces + cgroups) | Strong (hypervisor, separate kernel) |
| **Performance** | Native (no overhead) | ~2–10% overhead (hypervisor) |
| **Resource usage** | Lightweight (no duplicate OS) | Heavy (each VM runs full OS) |
| **Security boundary** | Kernel-level (shared) | Hardware-level (separate VM) |
| **Guest OS** | Same as host (e.g., Linux on Linux) | Any OS (Linux, Windows, BSD) |
| **Migration** | Limited (usually same host) | Live migration common |

## Docker & Linux Container Technology

### Underlying Kernel Features
- **Namespaces:** isolate process view of system
  | Namespace | Isolates | `lsns` |
  |-----------|----------|--------|
  | **PID** | Process IDs (pids) | `unshare --pid` |
  | **NET** | Network stack (interfaces, routes, iptables) | `unshare --net` |
  | **MNT** | Mount points (filesystem) | `unshare --mount` |
  | **UTS** | Hostname, domain name | `unshare --uts` |
  | **IPC** | System V IPC, POSIX message queues | `unshare --ipc` |
  | **USER** | User IDs (UID/GID mapping) | `unshare --user` |
  | **CGROUP** | cgroup hierarchy | `unshare --cgroup` |

- **cgroups (Control Groups):** limit resources per process group
  - `cpu.weight` — CPU shares
  - `memory.max` — memory limit (hard)
  - `memory.high` — memory limit (soft, triggers reclaim)
  - `io.weight` — I/O bandwidth

### Union Filesystem (OverlayFS)
- **Layers:** read-only image layers + read-write container layer
- **CoW (Copy-on-Write):** writes go to top layer (don't modify base)
- `overlay2`: default Docker storage driver (merge upper + lower dirs)

## Security Considerations

| Aspect | Container | VM |
|--------|-----------|-----|
| **Attack surface** | Large (shared kernel) | Small (hypervisor only) |
| **Escape risk** | Container → host (kernel bug) | VM → hypervisor (rare) |
| **Default isolation** | Process-level (namespaces) | Hardware-level (hypervisor) |
| **Recommendation** | Rootless, seccomp, AppArmor | For untrusted workloads |

- **gVisor:** user-space kernel intercepts syscalls (defense-in-depth)
- **Kata Containers:** lightweight VMs with container interface

## Kubernetes (Container Orchestration)
- **Pod:** smallest unit (one or more containers sharing network + storage)
- **Node:** worker machine (runs kubelet, container runtime)
- **Control plane:** API server, scheduler, controller manager, etcd
- **Runtime:** Docker, containerd, CRI-O

## Container vs VM Decision

| Use Case | Choose |
|----------|--------|
| Microservices, CI/CD, dev | Container |
| Multi-tenant, untrusted code | VM |
| Run different OS | VM |
| High-density deployment | Container |
| Strong security isolation | VM (or Kata/gVisor) |

## Interview Tips
- *"Containers share the host kernel — lightweight but weaker isolation"*
- *"VMs provide hardware-level isolation with separate kernels"*
- *"Docker uses namespaces for isolation, cgroups for resource limits, OverlayFS for layers"*
- *"Kubernetes orchestrates containers — pods, deployments, services"*
