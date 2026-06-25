# System Call Implementation

## What is a System Call?
- **Controlled entry** from user space into kernel space
- Request for kernel service (file I/O, process creation, network)
- User cannot access kernel memory directly

## Transition Mechanism (x86_64)
- Old: `int 0x80` (slow, involves interrupt table lookup)
- Modern: **`syscall`** instruction (faster: fewer cycles, no interrupt)
  - `RCX` = return address, `R11` = saved RFLAGS
  - `MSR_LSTAR` holds syscall entry point
  - Returns via `sysret` instruction

## System Call Process
1. User program calls **glibc wrapper** (e.g., `write()`)
2. Wrapper saves args in registers, sets syscall number in `rax`
3. Executes **`syscall`** → CPU switches to ring 0
4. Kernel saves registers → looks up `sys_call_table[rax]`
5. Calls handler function (e.g., `sys_write()`)
6. Returns result in `rax` → switches to ring 3
7. Wrapper checks error, returns to user

## Syscall Table
- `arch/x86/entry/syscalls/syscall_64.tbl`: maps number → name → handler
- Example: `0 → read → sys_read`, `1 → write → sys_write`
- Dynamic entries for architecture-specific syscalls

## Error Handling
- Syscall returns **negative value** on error (e.g., `-EINVAL`)
- glibc wrapper negates it, stores in `errno`, returns -1
- Common errors: `EINVAL`, `EFAULT`, `EAGAIN`, `ENOMEM`, `EACCES`

## Key Kernel Functions
```c
// Generic syscall handler
asmlinkage long sys_write(unsigned int fd,
                          const char __user *buf,
                          size_t count);
```
- `asmlinkage`: function receives args on stack (not registers)
- `__user`: annotation (not enforced, but sparse checker uses it)

## Adding a New Syscall
1. Add entry to syscall table
2. Implement handler function
3. Update header files for glibc
4. Rebuild kernel and glibc (rarely done — use modules or ioctl instead)
