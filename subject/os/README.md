# Operating System — Complete Interview Guide

**Target**: FAANG | MAANG | Tesla | SpaceX | Top YC Startups | High-Level Startups

---

## 📚 Study Roadmap (Fast Track)

### Phase 1: Fundamentals (Day 1-2)
| Topic | Files |
|-------|-------|
| Process Basics | `01-processes-and-threads/01-process-basics/` |
| Threads | `01-processes-and-threads/02-threads/` |
| CPU Scheduling | `01-processes-and-threads/03-process-scheduling/` |
| IPC | `01-processes-and-threads/04-interprocess-communication/` |

### Phase 2: Concurrency & Sync (Day 3-4)
| Topic | Files |
|-------|-------|
| Critical Section | `02-process-synchronization/01-critical-section/` |
| Semaphores | `02-process-synchronization/02-semaphores/` |
| Monitors | `02-process-synchronization/03-monitors/` |
| Locks | `02-process-synchronization/04-locks/` |
| Deadlocks | `03-deadlocks/` |
| Concurrency | `10-concurrency-and-parallelism/` |

### Phase 3: Memory (Day 5-6)
| Topic | Files |
|-------|-------|
| Memory Basics | `04-memory-management/01-memory-management-basics/` |
| Paging | `04-memory-management/02-pagination/` |
| Segmentation | `04-memory-management/03-segmentation/` |
| Virtual Memory | `04-memory-management/04-virtual-memory/` |

### Phase 4: Storage & I/O (Day 7-8)
| Topic | Files |
|-------|-------|
| File System Interface | `05-file-system/01-file-system-interface/` |
| File System Implementation | `05-file-system/02-file-system-implementation/` |
| Disk Management | `05-file-system/03-free-space-management/` to `05-file-system/05-raid/` |
| I/O Management | `06-io-management/` |

### Phase 5: Advanced (Day 9-10)
| Topic | Files |
|-------|-------|
| Security & Protection | `07-security-and-protection/` |
| Distributed Systems | `08-distributed-systems/` |
| Linux Internals | `09-linux-internals/` |
| Virtualization & RTOS | `12-advanced-topics/` |

### Phase 6: Interview Prep (Day 11-12)
| Topic | Files |
|-------|-------|
| Quick Revision | `11-interview-specific/01-quick-revision/` |
| Code Snippets | `11-interview-specific/02-code-snippets/` |
| Company-Specific | `11-interview-specific/03-company-specific/` |

---

## 📂 Complete Structure

```
subject/os/
├── 01-processes-and-threads/
│   ├── 01-process-basics/
│   │   ├── process-concept.md
│   │   ├── process-states.md
│   │   └── process-control-block.md
│   ├── 02-threads/
│   │   ├── thread-models.md
│   │   └── multithreading-models.md
│   ├── 03-process-scheduling/
│   │   ├── scheduling-criteria.md
│   │   ├── fcfs-sjf.md
│   │   ├── priority-round-robin.md
│   │   └── multilevel-queue-feedback.md
│   └── 04-interprocess-communication/
│       ├── shared-memory.md
│       ├── message-passing.md
│       └── pipes-and-signals.md
│
├── 02-process-synchronization/
│   ├── 01-critical-section/
│   │   ├── peterson-solution.md
│   │   └── hardware-synchronization.md
│   ├── 02-semaphores/
│   │   ├── semaphore-basics.md
│   │   ├── classic-problems.md
│   │   └── deadlock-starvation.md
│   ├── 03-monitors/
│   │   └── monitor-implementation.md
│   └── 04-locks/
│       ├── mutex-vs-semaphore.md
│       ├── spinlocks.md
│       └── read-write-locks.md
│
├── 03-deadlocks/
│   ├── 01-deadlock-characterization/
│   │   ├── necessary-conditions.md
│   │   └── resource-allocation-graph.md
│   ├── 02-deadlock-prevention/
│   │   └── prevention-strategies.md
│   ├── 03-deadlock-avoidance/
│   │   ├── safe-state.md
│   │   └── bankers-algorithm.md
│   ├── 04-deadlock-detection/
│   │   ├── detection-algorithms.md
│   │   └── recovery-from-deadlock.md
│   └── 05-deadlock-in-practice/
│       └── deadlock-in-databases-and-os.md
│
├── 04-memory-management/
│   ├── 01-memory-management-basics/
│   │   ├── swapping.md
│   │   └── contiguous-allocation.md
│   ├── 02-pagination/
│   │   ├── basic-pagination.md
│   │   ├── page-table-implementation.md
│   │   ├── hierarchical-pagetable.md
│   │   └── hashed-and-inverted-pagetable.md
│   ├── 03-segmentation/
│   │   └── segmentation-basics.md
│   └── 04-virtual-memory/
│       ├── demand-paging.md
│       ├── page-replacement-algorithms-fifo.md
│       ├── page-replacement-algorithms-optimal.md
│       ├── page-replacement-algorithms-lru.md
│       ├── page-replacement-algorithms-lru-approximation.md
│       ├── page-replacement-summary.md
│       ├── thrashing.md
│       ├── working-set-model.md
│       └── memory-mapped-files.md
│
├── 05-file-system/
│   ├── 01-file-system-interface/
│   │   ├── file-concept.md
│   │   ├── access-methods.md
│   │   └── directory-structure.md
│   ├── 02-file-system-implementation/
│   │   ├── file-system-structure.md
│   │   ├── directory-implementation.md
│   │   └── allocation-methods.md
│   ├── 03-free-space-management/
│   │   └── free-space-management.md
│   ├── 04-disk-scheduling/
│   │   ├── fcfs-sstf-scan-c-scan.md
│   │   └── look-c-look.md
│   ├── 05-raid/
│   │   └── raid-levels.md
│   └── 06-file-system-implementations/
│       ├── fat.md
│       └── ext4-ntfs.md
│
├── 06-io-management/
│   ├── 01-io-hardware/
│   │   └── io-hardware-basics.md
│   ├── 02-io-software/
│   │   └── io-software-layers.md
│   ├── 03-dma/
│   │   └── direct-memory-access.md
│   └── 04-kernel-io-subsystem/
│       ├── io-scheduling.md
│       ├── buffering.md
│       ├── caching.md
│       └── spooling.md
│
├── 07-security-and-protection/
│   ├── 01-security-threats/
│   │   ├── security-threats.md
│   │   ├── authentication.md
│   │   └── encryption.md
│   └── 02-protection-models/
│       ├── access-matrix.md
│       └── acl.md
│
├── 08-distributed-systems/
│   ├── 01-distributed-system-basics/
│   │   ├── distributed-system-types.md
│   │   └── network-topology.md
│   ├── 02-distributed-synchronization/
│   │   ├── clock-synchronization.md
│   │   ├── mutual-exclusion.md
│   │   └── election-algorithms.md
│   └── 03-distributed-file-systems/
│       ├── DFS-architecture.md
│       └── naming-and-caching.md
│
├── 09-linux-internals/
│   ├── 01-linux-architecture/
│   │   └── linux-architecture-overview.md
│   ├── 02-linux-process-management/
│   │   ├── process-creation.md
│   │   └── scheduling-in-linux.md
│   ├── 03-linux-memory-management/
│   │   └── memory-management-linux.md
│   ├── 04-linux-file-system/
│   │   ├── vfs.md
│   │   └── ext4-details.md
│   ├── 05-system-calls/
│   │   ├── system-call-implementation.md
│   │   └── important-syscalls.md
│   └── 06-linux-ipc/
│       ├── pipes.md
│       ├── fifos.md
│       ├── shared-memory-linux.md
│       ├── message-queues.md
│       └── sockets.md
│
├── 10-concurrency-and-parallelism/
│   ├── 01-amdahls-law.md
│   ├── 02-mutex-implementations.md
│   ├── 03-lock-free-data-structures.md
│   ├── 04-actor-model.md
│   └── 05-c10k-problem.md
│
├── 11-interview-specific/
│   ├── 01-quick-revision/
│   │   ├── process-vs-thread.md
│   │   ├── user-vs-kernel-thread.md
│   │   ├── types-of-ipc.md
│   │   ├── types-of-schedulers.md
│   │   ├── types-of-memory.md
│   │   ├── fragmentation.md
│   │   ├── starvation-vs-deadlock.md
│   │   ├── concurrency-vs-parallelism.md
│   │   └── types-of-kernels.md
│   ├── 02-code-snippets/
│   │   ├── producer-consumer.md
│   │   ├── dining-philosophers.md
│   │   ├── readers-writers.md
│   │   ├── bounded-buffer.md
│   │   └── thread-pool.md
│   └── 03-company-specific/
│       ├── google-os-topics.md
│       ├── amazon-os-topics.md
│       ├── microsoft-os-topics.md
│       ├── meta-os-topics.md
│       └── netflix-uber-lyft.md
│
├── 12-advanced-topics/
│   ├── 01-virtualization/
│   │   ├── hypervisors.md
│   │   ├── containers-vs-vms.md
│   │   └── docker-basics.md
│   ├── 02-real-time-systems/
│   │   ├── rtos-characteristics.md
│   │   └── priority-inversion.md
│   └── 03-mobile-os/
│       ├── android-architecture.md
│       └── ios-architecture.md
│
└── README.md (this file)
```

---

## ⚡ Quick Revision Strategy

1. **Morning**: Read `11-interview-specific/01-quick-revision/` (all 9 files — 30 min)
2. **Afternoon**: Practice code from `11-interview-specific/02-code-snippets/` (write code blind)
3. **Evening**: Read one company file from `11-interview-specific/03-company-specific/`
4. **Repeat daily** until interview

---

## 🔥 Most Frequently Asked Topics at Top Companies

| Company | Hot Topics |
|---------|-----------|
| **Google** | Scheduling, Memory Mgmt, Concurrency, Distributed Systems |
| **Amazon** | Virtualization, Containers, Distributed FS, I/O |
| **Microsoft** | NT Kernel, Windows Scheduling, I/O Completion Ports |
| **Meta** | Page Cache, NUMA, Kernel Tuning, Shared Memory |
| **Netflix** | Microservices, Caching, CDN, I/O Performance |
| **Uber/Lyft** | RPC Frameworks, Distributed Storage, Service Mesh |
| **Tesla/SpaceX** | RTOS, Priority Inversion, Embedded Systems |
| **YC Startups** | Concurrency, Scalability, Containers, Systems Design |

---

**Total**: 120 files covering every topic from basics to advanced, interview-focused.
