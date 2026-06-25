# Android OS Architecture

## System Architecture

```
┌──────────────────────────────────────────────┐
│  Applications (System UI, Dialer, Chrome...)  │
├──────────────────────────────────────────────┤
│  Android Framework (Java API)                │
│  ├── Activity Manager, Window Manager         │
│  ├── Content Providers, View System           │
│  ├── Package Manager, Telephony Manager       │
│  └── Location, Notification, etc.             │
├──────────────────────────────────────────────┤
│  Android Runtime (ART) + Native Libs         │
│  ART (AOT+JIT), libc, SSL, media, OpenGL...   │
├──────────────────────────────────────────────┤
│  Hardware Abstraction Layer (HAL)             │
│  Camera, Audio, GPS, Sensors (vendor impl)    │
├──────────────────────────────────────────────┤
│  Linux Kernel (modified)                      │
│  Binder, ashmem, wakelocks, LMK, cgroups...  │
└──────────────────────────────────────────────┘
```

## Key Components

### ART (Android Runtime)
- **AOT (Ahead-of-Time):** bytecode → native (during install)
- **JIT (Just-in-Time):** hot methods compiled at runtime (profile-guided)
- **GC:** concurrent mark-sweep, compacting (reduces fragmentation)
- **Replaced Dalvik** (Android 5.0+)

### Binder IPC
- Android's primary IPC mechanism (RPC-like)
- Uses **shared memory** + **ioctl** on `/dev/binder`
- **Binder driver** in kernel (not a standard Linux IPC)
- **Transaction:** client → driver → service (with marshalling)
- Each Android service registers with **Service Manager**

### Activity Lifecycle
```
onCreate() → onStart() → onResume() → RUNNING
                                  ↓
    onPause() → onStop() → onDestroy()
         ↓           ↓
    onResume()  onRestart()
```
- **Paused:** partially visible (system may kill in low memory)
- **Stopped:** not visible (may be killed)
- **onSaveInstanceState()** preserves state across rotation/kill

## Memory Management
| Feature | Description |
|---------|-------------|
| **LMK (Low Memory Killer)** | Kills processes based on priority (oom_adj) when memory low |
| **ashmem** | Anonymous shared memory (file descriptor based) |
| **cgroups v1** | Used for memory accounting (Android 10+ uses cgroups v2) |
| **ZRAM** | Compressed swap in RAM (not disk swap) |

## App Sandbox
- Each app = **separate Linux user ID** (UID)
- Runs in **isolated process** (different UID = different permissions)
- **Files:** per-app directory, not world-readable
- **Permissions:** declared in manifest, user grants at runtime (Android 6+)
- **SELinux:** mandatory access control (enforcing since Android 5)

## Power Management
- **Wakelocks:** prevent device from sleeping (app requests via `PowerManager`)
- **Doze mode:** deep sleep when device stationary (Android 6+)
- **App Standby:** background apps restricted (network, CPU, alarms)

## Interview Tips
- *"Android uses Linux kernel but adds Binder IPC, ashmem, LMK, and wakelocks"*
- *"ART compiles bytecode to native at install time (AOT) + hot method JIT"*
- *"App sandbox: each app = separate Linux UID, SELinux enforced, permission-gated"*
- *"Low Memory Killer kills processes by priority (oom_adj) — no swap"*
- *"Binder is Android's secret sauce for IPC"*
