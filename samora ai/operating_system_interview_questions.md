# Operating System Interview Questions (Top 100)

## 1. What is an operating system?
An OS is system software managing hardware resources and providing services to applications.

## 2. What are the main functions of an OS?
Process management, memory management, file system, device management, and security.

## 3. What is a process?
A process is an executing instance of a program with its own memory space and resources.

## 4. What is a thread?
A thread is the smallest unit of execution within a process, sharing the process's memory.

## 5. Difference between process and thread.
Processes are independent with separate memory; threads share memory within a process.

## 6. What is a program versus process?
A program is static code on disk; a process is the running execution of that program.

## 7. What are the states of a process?
New, Ready, Running, Waiting (Blocked), Terminated.

## 8. What is a Process Control Block (PCB)?
A data structure holding process info: state, registers, PID, memory, scheduling data.

## 9. What is context switching?
Saving the state of a running process and loading another's state for CPU switching.

## 10. What is a context switch overhead?
Time and resources consumed during switching, which does not perform useful work.

## 11. What is scheduling?
The OS deciding which process or thread gets CPU time.

## 12. What are common CPU scheduling algorithms?
FCFS, SJF, Priority, Round Robin, Multilevel Queue.

## 13. What is FCFS?
First-Come First-Served: processes served in arrival order; simple but can cause convoy effect.

## 14. What is SJF?
Shortest Job First: picks the process with the smallest burst time; optimal but may starve.

## 15. What is Round Robin scheduling?
Each process gets a fixed time quantum cyclically; fair and responsive.

## 16. What is Priority scheduling?
Processes served by priority; can be preemptive or non-preemptive; risk of starvation.

## 17. What is a time quantum?
The maximum time a process runs before being preempted in Round Robin.

## 18. What is throughput?
Number of processes completed per unit time.

## 19. What is turnaround time?
Time from process submission to completion.

## 20. What is waiting time?
Time a process spends in the ready queue (turnaround minus burst).

## 21. What is response time?
Time from submission to first response (important for interactive systems).

## 22. What is a race condition?
When multiple processes access shared data concurrently and the outcome depends on timing.

## 23. What is a critical section?
A code segment accessing shared resources that must not run concurrently.

## 24. What are the requirements for a solution to critical section?
Mutual exclusion, progress, bounded waiting, and no assumptions about speed.

## 25. What is mutual exclusion?
Only one process can be in its critical section at a time.

## 26. What is a semaphore?
A synchronization primitive (integer + wait or signal) controlling access to resources.

## 27. What is a binary semaphore?
A semaphore with values 0 or 1, acting like a mutex.

## 28. What is a counting semaphore?
A semaphore with a non-negative count for managing multiple resource instances.

## 29. What is a mutex?
A locking mechanism ensuring exclusive access; only the owner can unlock it.

## 30. Difference between semaphore and mutex.
Semaphore signals or counters for general sync; mutex is for mutual exclusion with ownership.

## 31. What is deadlock?
A set of processes each waiting for resources held by another, with no progress.

## 32. What are the four Coffman conditions for deadlock?
Mutual exclusion, hold and wait, no preemption, circular wait.

## 33. How can deadlock be handled?
Prevention, avoidance, detection and recovery, or ignoring (ostrich approach).

## 34. What is deadlock prevention?
Ensuring at least one Coffman condition cannot hold (for example, eliminate hold-and-wait).

## 35. What is deadlock avoidance?
Dynamically checking resource allocation safety (for example, Banker's algorithm).

## 36. What is the Banker's algorithm?
A deadlock-avoidance algorithm that allocates resources only if the system stays safe.

## 37. What is deadlock detection?
The OS periodically checks for cycles in the resource graph and recovers.

## 38. What is starvation?
A process is indefinitely denied resources while others keep getting served.

## 39. What is aging in scheduling?
Gradually increasing priority of waiting processes to prevent starvation.

## 40. What is virtual memory?
A memory management technique giving processes an illusion of contiguous large memory.

## 41. What is paging?
Dividing memory and processes into fixed-size pages or frames, mapped by a page table.

## 42. What is a page table?
A structure mapping logical page numbers to physical frame numbers.

## 43. What is fragmentation?
Wasted memory: external (free gaps between allocations) or internal (unused within a block).

## 44. What is internal fragmentation?
Allocated memory block larger than needed, wasting space inside the block.

## 45. What is external fragmentation?
Free memory scattered in small pieces, unable to satisfy a contiguous request.

## 46. What is a page fault?
An access to a page not currently in physical memory, triggering a load from disk.

## 47. What is thrashing?
Excessive paging causing the system to spend more time swapping than executing.

## 48. What is demand paging?
Pages are loaded into memory only when accessed (on demand), not all upfront.

## 49. What is swapping?
Moving entire processes between main memory and disk to free RAM.

## 50. What is a cache?
A small fast memory storing frequently accessed data to reduce access time.

## 51. What is the difference between RAM and ROM?
RAM is volatile and writable; ROM is non-volatile and typically read-only.

## 52. What is a file system?
A method for storing, organizing, and retrieving files on storage devices.

## 53. What are common file systems?
FAT32, NTFS, ext4, APFS, HFS+, ZFS.

## 54. What is an inode?
A Unix data structure holding file metadata (permissions, size, pointers) excluding name.

## 55. What is a directory?
A special file containing references to other files (a folder).

## 56. What is a system call?
An interface for user programs to request OS services (for example, read, write, fork).

## 57. What are types of system calls?
Process control, file manipulation, device, information maintenance, communication.

## 58. What is a kernel?
The core of the OS managing system resources and hardware interaction.

## 59. What is a monolithic kernel?
A kernel where all services run in kernel space (for example, Linux); fast but less modular.

## 60. What is a microkernel?
A minimal kernel with most services in user space (for example, Mach); more modular and secure.

## 61. What is a hybrid kernel?
Combines monolithic and microkernel features (for example, Windows NT, macOS XNU).

## 62. What is user mode versus kernel mode?
User mode restricts access; kernel mode has full hardware access; switch via system call.

## 63. What is an interrupt?
A signal to the CPU to pause current work and handle an event.

## 64. What is a trap?
A software-generated interrupt (for example, system call or error) transferring to kernel mode.

## 65. What is a device driver?
Software enabling the OS to communicate with hardware devices.

## 66. What is spooling?
Queueing jobs (for example, print) to a buffer so devices process them without blocking.

## 67. What is a daemon?
A background process running without user interaction (for example, cron).

## 68. What is IPC?
Inter-Process Communication: mechanisms for processes to exchange data.

## 69. What are IPC methods?
Pipes, message queues, shared memory, semaphores, sockets, signals.

## 70. What is a pipe?
A unidirectional channel connecting the output of one process to another.

## 71. What is shared memory IPC?
Processes map the same memory region to communicate fastest without copying.

## 72. What is a signal?
A limited asynchronous notification sent to a process (for example, SIGKILL, SIGTERM).

## 73. What is a socket?
An endpoint for communication between processes across a network or locally.

## 74. What is producer-consumer problem?
A classic sync problem where producers add and consumers remove from a bounded buffer.

## 75. What is the readers-writers problem?
Coordinating processes that read (many) and write (exclusive) shared data.

## 76. What is the dining philosophers problem?
A classic deadlock example with philosophers alternating thinking and eating with shared forks.

## 77. What is a real-time operating system (RTOS)?
An OS guaranteeing timely responses within strict deadlines (for example, embedded systems).

## 78. What is a batch operating system?
Processes jobs in batches without user interaction (early mainframes).

## 79. What is a time-sharing OS?
Multiple users share the CPU via rapid switching for interactivity.

## 80. What is a distributed OS?
An OS managing a network of machines appearing as a single coherent system.

## 81. What is multiprogramming?
Running multiple programs concurrently by overlapping their execution on one CPU.

## 82. What is multitasking?
The OS rapidly switching between tasks to give the illusion of parallelism.

## 83. What is multiprocessing?
Using more than one CPU slash core to execute processes truly in parallel.

## 84. What is parallelism versus concurrency?
Parallelism runs tasks simultaneously (multiple cores); concurrency interleaves over time.

## 85. What is a deadlock versus livelock?
Deadlock is stuck waiting; livelock is active but making no progress (repeated reacting).

## 86. What is TLB?
Translation Lookaside Buffer: a cache speeding up virtual-to-physical address translation.

## 87. What is address binding?
Mapping program addresses to physical memory addresses (compile, load, execution time).

## 88. What is logical versus physical address?
Logical (virtual) is generated by CPU; physical is the actual memory location.

## 89. What is contiguous versus non-contiguous memory allocation?
Contiguous places a process in one block; non-contiguous (paging or segmentation) splits it.

## 90. What is segmentation?
Dividing memory into variable-sized segments by logical units (code, stack, data).

## 91. Difference between paging and segmentation.
Paging uses fixed-size blocks (no external frag); segmentation uses logical variable blocks.

## 92. What is a bootloader?
Code that loads the OS kernel into memory during startup.

## 93. What is BIOS slash UEFI?
Firmware initializing hardware and starting the boot process.

## 94. What is the difference between process and program in memory?
Program is code on disk; process has text, data, heap, and stack segments in RAM.

## 95. What is a zombie process?
A terminated process whose entry remains until the parent reads its exit status.

## 96. What is an orphan process?
A process whose parent terminated; usually adopted by init or systemd.

## 97. What is fork()?
A system call creating a child process as a copy of the parent (Unix).

## 98. What is a thread pool?
A set of pre-created threads reused to handle tasks, reducing creation overhead.

## 99. What is the difference between user-level and kernel-level threads?
User threads managed by a library; kernel threads scheduled by the OS; many-to-one or one-to-one mapping.

## 100. What are the benefits of multithreading?
Responsiveness, resource sharing, economy (less overhead than processes), and parallelism on multicore.
