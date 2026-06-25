# Multithreading Models

## 1. Many-to-One Model

```
User threads    T1    T2    T3
                 \    |    /
Kernel thread     ┌───┴───┐
                  │  K1   │
                  └───────┘
```

| Aspect | Detail |
|--------|--------|
| **Mapping** | Many user threads → 1 kernel thread |
| **Kernel aware?** | No — kernel sees only one process |
| **Concurrency** | ✅ User-level concurrency (library schedules) |
| **Parallelism** | ❌ Cannot run on multiple CPUs |
| **Blocking** | ❌ One blocking thread → entire process blocks |
| **Use case** | Legacy systems, embedded (no kernel threading support) |
| **Example** | Solaris Green Threads, GNU Pth |

## 2. One-to-One Model

```
User threads    T1       T2       T3
                │        │        │
Kernel threads  │        │        │
              ┌─┴─┐    ┌─┴─┐    ┌─┴─┐
              │ K1│    │ K2│    │ K3│
              └───┘    └───┘    └───┘
```

| Aspect | Detail |
|--------|--------|
| **Mapping** | 1 user thread → 1 kernel thread |
| **Parallelism** | ✅ True parallelism on multi-core |
| **Blocking** | ✅ One thread blocks, others unaffected |
| **Overhead** | Creating kernel threads is expensive (syscall per thread) |
| **Limit** | Usually limited by OS (e.g., thousands, not millions) |
| **Used by** | **Linux NPTL**, **Windows**, **macOS** |

## 3. Many-to-Many Model

```
User threads    T1    T2    T3      T4    T5
                 \   /      \      /      \
                  ┌─┐        ┌──┐        ┌─┐
Kernel threads    │K1│        │K2│        │K3│
                  └─┘        └──┘        └─┘
```

| Aspect | Detail |
|--------|--------|
| **Mapping** | Many user threads → Many kernel threads (often fewer kernel threads) |
| **Parallelism** | ✅ Can utilize multiple CPUs |
| **Flexibility** | OS can multiplex many user threads onto fewer kernel threads |
| **Complexity** | High — scheduler must manage two levels |
| **Example** | Solaris (prior to Solaris 9), IRIX |

## 4. Two-Level Model

```
User threads    T1    T2    T3      T4    T5    T6
                 \   /      \      /      \    /
                  ┌─┐        ┌──┐        ┌──┐
Kernel threads    │K1│        │K2│        │K3│    (K4 bound to T6)
                  └─┘        └──┘        └──┘
```

- Hybrid: Many-to-Many + ability to **bind** a user thread to one kernel thread
- Important threads can get dedicated kernel thread (e.g., GUI thread)
- Used in **Solaris 9** and later

## Comparison Table

| Model | Concurrency | Parallelism | Blocking | Kernel Overhead | Real-World |
|-------|------------|-------------|----------|-----------------|------------|
| **Many-to-One** | ✅ | ❌ | ❌ (blocks all) | Minimal | Legacy only |
| **One-to-One** | ✅ | ✅ | ✅ | High (per thread) | **Linux, Windows, macOS** |
| **Many-to-Many** | ✅ | ✅ | ✅ | Moderate | Solaris (historical) |
| **Two-Level** | ✅ | ✅ | ✅ | Moderate | Solaris 9+ |

### 🎯 Interview Tip
- Linux uses **one-to-one** via NPTL (since glibc 2.3.2, kernel 2.6)
- 1M+ threads at high memory cost (~8 MB stack per thread default)
- **goroutines** (Go) emulate many-to-many — userspace green threads multiplexed onto OS threads
