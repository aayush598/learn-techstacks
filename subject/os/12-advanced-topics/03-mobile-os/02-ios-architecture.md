# iOS & macOS OS Architecture

## XNU Kernel (X is Not Unix)
**XNU = Mach microkernel + FreeBSD + IOKit (C++ driver framework)**

```
User Space
  ┌────────────────────────────────────┐
  │  Applications, Frameworks (Cocoa)  │
  └──────────────────┬─────────────────┘
                     │ (system calls, Mach traps)
Kernel Space ┌───────▼─────────────────────────┐
             │  BSD Layer                       │
             │  (processes, signals, file system,│
             │   networking, POSIX, Pthreads)    │
             ├──────────────────────────────────┤
             │  Mach Layer                       │
             │  (IPC, scheduler, VM, exceptions) │
             ├──────────────────────────────────┤
             │  IOKit (C++ drivers)              │
             └──────────────────────────────────┘
                     │
             Hardware (ARM64 / x86_64)
```

### Mach (Microkernel Layer)
- **Tasks** (processes) — own address space + ports
- **Threads** — unit of execution within task
- **Ports** — IPC endpoint (kernel-protected, capability-based)
- **Messages** — data sent between ports (copy-on-write via VM)
- **Scheduler** — CFS-like with priority (0–127)
- **VM subsystem** — Mach VM (mappable regions, paging)

### BSD Layer
- **Process model:** fork/exec, signals, POSIX API
- **Pthreads** (implemented on top of Mach threads)
- **File system:** Virtual File System (VFS) + APFS
- **Networking:** BSD socket layer (TCP/IP stack)

## Architecture Layers (iOS)

```
┌──────────────────────────────┐
│  Cocoa Touch (UIKit, SwiftUI)│
├──────────────────────────────┤
│  Media (AVFoundation, CoreML)│
├──────────────────────────────┤
│  Core Services (CoreData,    │
│  Foundation, CloudKit)       │
├──────────────────────────────┤
│  Core OS (XNU kernel,        │
│  Security, Power Mgmt)       │
└──────────────────────────────┘
```

## iOS Memory Management
- **jetsam:** memory pressure handler (kills processes)
  - On memory pressure: kill background → suspended → foreground (in order)
  - Processes have **jetsam priority** (foreground = highest)
- **No swap** (iOS devices don't have disk-backed virtual memory)
  - **Compressed memory:** compress inactive pages (WKdm compression)
- **page-based** VM: 16KB pages on ARM64 (4KB on macOS)

## Security Architecture
| Feature | Description |
|---------|-------------|
| **Secure Enclave** | Separate coprocessor (SEP) for biometrics, keys |
| **Code Signing** | All apps must be signed (verified before execution) |
| **Sandbox** | Container per app (app group, entitlements) |
| **Data Protection** | File encryption with class keys (NSFileProtection) |
| **ASLR** | Address Space Layout Randomization (full) |

## App Sandbox
- **Container:** per-app directory with randomized UUID
- **Entitlements:** capabilities granted to app (push, iCloud, etc.)
- **Access:** limited to own container, plus user-granted permissions (photos, location, etc.)
- **XPC services:** IPC between sandboxed processes

## APFS (Apple File System)
- **Copy-on-write:** modifications don't overwrite original blocks
- **Snapshots:** point-in-time read-only views
- **Cloning:** instant file/directory copies (CoW metadata)
- **Space sharing:** multiple volumes share same partition
- **Encryption:** per-file key, per-extent key (privacy)
- **Replaces HFS+** since macOS 10.13 / iOS 10.3

## Interview Tips
- *"XNU = Mach (IPC, scheduler, VM) + BSD (POSIX, FS, networking) + IOKit (drivers)"*
- *"Mach ports are the fundamental IPC primitive — used for everything"*
- *"iOS uses compressed memory (no swap); jetsam kills processes under pressure"*
- *"Secure Enclave is a separate processor for security-sensitive operations"*
- *"APFS is CoW with snapshots, cloning, and per-file encryption"*
