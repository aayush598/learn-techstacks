# Operating System — 100 Interview Q&A

---

## Q1: What is an operating system?
**A:** An OS is system software managing hardware resources and providing services to applications.

## Q2: What are the main functions of an OS?
**A:** Process management, memory management, file system, device management, and security.

## Q3: What is a process?
**A:** A process is an executing instance of a program with its own memory space and resources.

## Q4: What is a thread?
**A:** A thread is the smallest unit of execution within a process, sharing the process's memory.

## Q5: Difference between process and thread.
**A:** Processes are independent with separate memory; threads share memory within a process.

## Q6: What is a program versus process?
**A:** A program is static code on disk; a process is the running execution of that program.

## Q7: What are the states of a process?
**A:** New, Ready, Running, Waiting (Blocked), Terminated.

## Q8: What is a Process Control Block (PCB)?
**A:** A data structure holding process info: state, registers, PID, memory, scheduling data.

## Q9: What is context switching?
**A:** Saving the state of a running process and loading another's state for CPU switching.

## Q10: What is a context switch overhead?
**A:** Time and resources consumed during switching, which does not perform useful work.

## Q11: What is scheduling?
**A:** The OS deciding which process or thread gets CPU time.

## Q12: What are common CPU scheduling algorithms?
**A:** FCFS, SJF, Priority, Round Robin, Multilevel Queue.

## Q13: What is FCFS?
**A:** First-Come First-Served: processes served in arrival order; simple but can cause convoy effect.

## Q14: What is SJF?
**A:** Shortest Job First: picks the process with the smallest burst time; optimal but may starve.

## Q15: What is Round Robin scheduling?
**A:** Each process gets a fixed time quantum cyclically; fair and responsive.

## Q16: What is Priority scheduling?
**A:** Processes served by priority; can be preemptive or non-preemptive; risk of starvation.

## Q17: What is a time quantum?
**A:** The maximum time a process runs before being preempted in Round Robin.

## Q18: What is throughput?
**A:** Number of processes completed per unit time.

## Q19: What is turnaround time?
**A:** Time from process submission to completion.

## Q20: What is waiting time?
**A:** Time a process spends in the ready queue (turnaround minus burst).

## Q21: What is response time?
**A:** Time from submission to first response (important for interactive systems).

## Q22: What is a race condition?
**A:** When multiple processes access shared data concurrently and the outcome depends on timing.

## Q23: What is a critical section?
**A:** A code segment accessing shared resources that must not run concurrently.

## Q24: What are the requirements for a solution to critical section?
**A:** Mutual exclusion, progress, bounded waiting, and no assumptions about speed.

## Q25: What is mutual exclusion?
**A:** Only one process can be in its critical section at a time.

## Q26: What is a semaphore?
**A:** A synchronization primitive (integer + wait or signal) controlling access to resources.

## Q27: What is a binary semaphore?
**A:** A semaphore with values 0 or 1, acting like a mutex.

## Q28: What is a counting semaphore?
**A:** A semaphore with a non-negative count for managing multiple resource instances.

## Q29: What is a mutex?
**A:** A locking mechanism ensuring exclusive access; only the owner can unlock it.

## Q30: Difference between semaphore and mutex.
**A:** Semaphore signals or counters for general sync; mutex is for mutual exclusion with ownership.

## Q31: What is deadlock?
**A:** A set of processes each waiting for resources held by another, with no progress.

## Q32: What are the four Coffman conditions for deadlock?
**A:** Mutual exclusion, hold and wait, no preemption, circular wait.

## Q33: How can deadlock be handled?
**A:** Prevention, avoidance, detection and recovery, or ignoring (ostrich approach).

## Q34: What is deadlock prevention?
**A:** Ensuring at least one Coffman condition cannot hold (for example, eliminate hold-and-wait).

## Q35: What is deadlock avoidance?
**A:** Dynamically checking resource allocation safety (for example, Banker's algorithm).

## Q36: What is the Banker's algorithm?
**A:** A deadlock-avoidance algorithm that allocates resources only if the system stays safe.

## Q37: What is deadlock detection?
**A:** The OS periodically checks for cycles in the resource graph and recovers.

## Q38: What is starvation?
**A:** A process is indefinitely denied resources while others keep getting served.

## Q39: What is aging in scheduling?
**A:** Gradually increasing priority of waiting processes to prevent starvation.

## Q40: What is virtual memory?
**A:** A memory management technique giving processes an illusion of contiguous large memory.

## Q41: What is paging?
**A:** Dividing memory and processes into fixed-size pages or frames, mapped by a page table.

## Q42: What is a page table?
**A:** A structure mapping logical page numbers to physical frame numbers.

## Q43: What is fragmentation?
**A:** Wasted memory: external (free gaps between allocations) or internal (unused within a block).

## Q44: What is internal fragmentation?
**A:** Allocated memory block larger than needed, wasting space inside the block.

## Q45: What is external fragmentation?
**A:** Free memory scattered in small pieces, unable to satisfy a contiguous request.

## Q46: What is a page fault?
**A:** An access to a page not currently in physical memory, triggering a load from disk.

## Q47: What is thrashing?
**A:** Excessive paging causing the system to spend more time swapping than executing.

## Q48: What is demand paging?
**A:** Pages are loaded into memory only when accessed (on demand), not all upfront.

## Q49: What is swapping?
**A:** Moving entire processes between main memory and disk to free RAM.

## Q50: What is a cache?
**A:** A small fast memory storing frequently accessed data to reduce access time.

## Q51: What is the difference between RAM and ROM?
**A:** RAM is volatile and writable; ROM is non-volatile and typically read-only.

## Q52: What is a file system?
**A:** A method for storing, organizing, and retrieving files on storage devices.

## Q53: What are common file systems?
**A:** FAT32, NTFS, ext4, APFS, HFS+, ZFS.

## Q54: What is an inode?
**A:** A Unix data structure holding file metadata (permissions, size, pointers) excluding name.

## Q55: What is a directory?
**A:** A special file containing references to other files (a folder).

## Q56: What is a system call?
**A:** An interface for user programs to request OS services (for example, read, write, fork).

## Q57: What are types of system calls?
**A:** Process control, file manipulation, device, information maintenance, communication.

## Q58: What is a kernel?
**A:** The core of the OS managing system resources and hardware interaction.

## Q59: What is a monolithic kernel?
**A:** A kernel where all services run in kernel space (for example, Linux); fast but less modular.

## Q60: What is a microkernel?
**A:** A minimal kernel with most services in user space (for example, Mach); more modular and secure.

## Q61: What is a hybrid kernel?
**A:** Combines monolithic and microkernel features (for example, Windows NT, macOS XNU).

## Q62: What is user mode versus kernel mode?
**A:** User mode restricts access; kernel mode has full hardware access; switch via system call.

## Q63: What is an interrupt?
**A:** A signal to the CPU to pause current work and handle an event.

## Q64: What is a trap?
**A:** A software-generated interrupt (for example, system call or error) transferring to kernel mode.

## Q65: What is a device driver?
**A:** Software enabling the OS to communicate with hardware devices.

## Q66: What is spooling?
**A:** Queueing jobs (for example, print) to a buffer so devices process them without blocking.

## Q67: What is a daemon?
**A:** A background process running without user interaction (for example, cron).

## Q68: What is IPC?
**A:** Inter-Process Communication: mechanisms for processes to exchange data.

## Q69: What are IPC methods?
**A:** Pipes, message queues, shared memory, semaphores, sockets, signals.

## Q70: What is a pipe?
**A:** A unidirectional channel connecting the output of one process to another.

## Q71: What is shared memory IPC?
**A:** Processes map the same memory region to communicate fastest without copying.

## Q72: What is a signal?
**A:** A limited asynchronous notification sent to a process (for example, SIGKILL, SIGTERM).

## Q73: What is a socket?
**A:** An endpoint for communication between processes across a network or locally.

## Q74: What is producer-consumer problem?
**A:** A classic sync problem where producers add and consumers remove from a bounded buffer.

## Q75: What is the readers-writers problem?
**A:** Coordinating processes that read (many) and write (exclusive) shared data.

## Q76: What is the dining philosophers problem?
**A:** A classic deadlock example with philosophers alternating thinking and eating with shared forks.

## Q77: What is a real-time operating system (RTOS)?
**A:** An OS guaranteeing timely responses within strict deadlines (for example, embedded systems).

## Q78: What is a batch operating system?
**A:** Processes jobs in batches without user interaction (early mainframes).

## Q79: What is a time-sharing OS?
**A:** Multiple users share the CPU via rapid switching for interactivity.

## Q80: What is a distributed OS?
**A:** An OS managing a network of machines appearing as a single coherent system.

## Q81: What is multiprogramming?
**A:** Running multiple programs concurrently by overlapping their execution on one CPU.

## Q82: What is multitasking?
**A:** The OS rapidly switching between tasks to give the illusion of parallelism.

## Q83: What is multiprocessing?
**A:** Using more than one CPU slash core to execute processes truly in parallel.

## Q84: What is parallelism versus concurrency?
**A:** Parallelism runs tasks simultaneously (multiple cores); concurrency interleaves over time.

## Q85: What is a deadlock versus livelock?
**A:** Deadlock is stuck waiting; livelock is active but making no progress (repeated reacting).

## Q86: What is TLB?
**A:** Translation Lookaside Buffer: a cache speeding up virtual-to-physical address translation.

## Q87: What is address binding?
**A:** Mapping program addresses to physical memory addresses (compile, load, execution time).

## Q88: What is logical versus physical address?
**A:** Logical (virtual) is generated by CPU; physical is the actual memory location.

## Q89: What is contiguous versus non-contiguous memory allocation?
**A:** Contiguous places a process in one block; non-contiguous (paging or segmentation) splits it.

## Q90: What is segmentation?
**A:** Dividing memory into variable-sized segments by logical units (code, stack, data).

## Q91: Difference between paging and segmentation.
**A:** Paging uses fixed-size blocks (no external frag); segmentation uses logical variable blocks.

## Q92: What is a bootloader?
**A:** Code that loads the OS kernel into memory during startup.

## Q93: What is BIOS slash UEFI?
**A:** Firmware initializing hardware and starting the boot process.

## Q94: What is the difference between process and program in memory?
**A:** Program is code on disk; process has text, data, heap, and stack segments in RAM.

## Q95: What is a zombie process?
**A:** A terminated process whose entry remains until the parent reads its exit status.

## Q96: What is an orphan process?
**A:** A process whose parent terminated; usually adopted by init or systemd.

## Q97: What is fork()?
**A:** A system call creating a child process as a copy of the parent (Unix).

## Q98: What is a thread pool?
**A:** A set of pre-created threads reused to handle tasks, reducing creation overhead.

## Q99: What is the difference between user-level and kernel-level threads?
**A:** User threads managed by a library; kernel threads scheduled by the OS; many-to-one or one-to-one mapping.

## Q100: What are the benefits of multithreading?
**A:** Responsiveness, resource sharing, economy (less overhead than processes), and parallelism on multicore.
