# Booting Process

> **TL;DR**: Booting is the handoff of control up a trust chain — CPU firmware (UEFI/BIOS) → bootloader (GRUB) → kernel image → kernel init → first user-space process (PID 1) — with each stage loading and validating the next, culminating in the OS managing the machine.

## 1. Why Does This Exist?
A computer's memory and CPU state are undefined at power-on — there is no OS in RAM yet, and the CPU doesn't know where code lives. Booting exists to solve the chicken-and-egg problem: *some* code must run first from non-volatile storage (firmware in ROM/flash), locate an OS on disk, load it into memory, and hand control to it. It must also be **secure** (verify the next stage against attack — Secure Boot), **robust** (recover from a failed stage), and **flexible** (choose among multiple OSes/kernels — GRUB menu).

## 2. How Does It Work?
The boot process is a chain of increasingly capable programs:
1. **Power-on reset**: CPU jumps to a fixed firmware address (UEFI or legacy BIOS on x86; SoC ROM elsewhere).
2. **Firmware (UEFI/BIOS)**: POST (power-on self-test), initializes the bare minimum (CPU, memory, interrupt controller, disks), and scans boot devices.
3. **Bootloader (GRUB/systemd-boot)**: runs on the firmware ABI; loads the kernel image (and initramfs/initrd) from disk into memory.
4. **Kernel handoff**: firmware/bootloader enters the kernel entry point (e.g., `startup_64`) in protected mode with the boot params passed.
5. **Kernel init**: decompresses itself, sets up page tables and early console, initializes subsystems (interrupts, scheduler, memory), mounts root filesystem, then spawns PID 1.
6. **Init (systemd)**: reads targets/units, mounts filesystems, starts services, launches login/getty.

## 3. When Is It Used?
- **Every cold boot** of a server, desktop, phone, or embedded device.
- **Virtual machine boot**: firmware (OVMF), bootloader, kernel — inside a VM.
- **Fast-boot / hibernation resume**: firmware skips full init and restores an image (Windows Fast Startup, `S4` hibernation).
- **Disaster recovery**: `init=/bin/bash` on kernel cmdline; single-user mode; kernel "rescue" via initramfs.
- **Container/host kernel upgrades**: kexec (`kexec -l` then `reboot`) reuses loaded kernel without full firmware re-init.
- **Secure environments**: UEFI Secure Boot verifies the bootloader signature; the bootloader verifies the kernel; initramfs may carry TPM measurement.

## 4. Why Wasn't Another Approach Chosen?
- **Whole OS in ROM** (like early embedded): too inflexible — can't update the OS, too little flash space, can't customize. Rejected; firmware is kept minimal.
- **Firmware loads the OS directly** (no bootloader): ties firmware to filesystem/OS details; bootloaders (GRUB) abstract that, support multiboot, menus, and scripts.
- **Kernel mapped directly from disk (no load into RAM)**: can't execute from most storage; loading into RAM is required; with compression, less RAM is needed.
- **CPU begins executing at a fixed disk address** (old PC BIOS behavior of loading sector 0 into 0x7C00): fragile and tiny (one sector = 512B). Modern UEFI boots from a partition with a full PE executable.
- **No verification** (no Secure Boot): trivially subverted by bootkits (e.g., Evil Maid). Modern platforms add signature verification at each stage.
The chosen design — staged handoff with signatures — balances flexibility, size, and security.

## 5. Intuition
Booting is like a **relay race with three runners**, each passing the baton only after reaching their checkpoint: UEFI (sprinter) checks the track and starts; GRUB (mid-distance) picks up the baton and runs the load; the kernel (marathoner) takes over for the long haul and then organizes the whole team (systemd) that keeps the race going. Each runner verifies the next one's identity (Secure Boot handshakes).

## 6. Real-World Analogy
A **ski lift / airport boarding chain**: you (CPU) start at the airport entrance (reset vector). Security (firmware) checks ID (POST). The shuttle (bootloader) takes you to the plane (kernel image). The pilot (kernel init) runs the checklist and starts engines (subsystems). Air traffic control (systemd/PID 1) then manages all the flights (services). If any checkpoint fails, you don't board — the machine won't boot (or falls to a rescue shell).

## 7. Formal Definition
**Booting** is the sequence of firmware- and software-controlled stages that transitions a computer from power-on (undefined CPU state) to a running operating system with a stable initial user-space (PID 1). Key stages: reset vector → firmware (BIOS/UEFI) POST & boot-device selection → bootloader (stage 1/stage 2) → kernel decompression & initialization (`start_kernel()`) → `kernel_init` → first user process (PID 1, `systemd`/`init`).

## 8. Example
Boot a Linux server with UEFI:
1. CPU resets, jumps to `0xFFFFFFF0` (UEFI platform firmware).
2. UEFI POST runs; discovers NVMe boot disk; reads the EFI System Partition (ESP).
3. UEFI Secure Boot verifies `\EFI\BOOT\BOOTX64.EFI` (GRUB) signature against db keys.
4. GRUB reads `/boot/grub/grub.cfg`, displays the menu, loads `vmlinuz-6.x` + `initramfs-6.x.img` via EFI runtime services.
5. GRUB calls the kernel with `ExitBootServices()`, jumping to `startup_64`.
6. Kernel: decompress → set up page tables → `start_kernel()`: `setup_arch` (console, timers), `init_IRQ`, `time_init`, `sched_init`, `mm_init`, `vfs_caches_init`, `rest_init` → `kernel_init` thread.
7. `kernel_init` mounts root from cmdline (`root=/dev/mapper/vg-root`), runs `/sbin/init` (systemd) as PID 1.
8. systemd: `default.target`, mounts everything, starts `sshd`, `docker`, etc.; getty on tty.

## 9. Internal Working
1. **Firmware**: UEFI DXE phase initializes hardware; BDS (boot device selection) loads the boot entry; EFI runtime services persist after boot.
2. **Bootloader**: GRUB — GRUB2 modules (`linux`, `normal`); reads filesystem from firmware or own drivers; loads kernel into RAM at `0x1000000+`; constructs `boot_params`/DTB; performs `ExitBootServices`.
3. **Kernel entry**: `arch/x86/boot/header.S` → protected mode; decompressor `arch/x86/boot/compressed`; `startup_64` in `arch/x86/kernel/head_64.S`.
4. **`start_kernel()`** (`init/main.c`): `setup_arch` → `mm_init` → `sched_init` → `init_IRQ` → `time_init` → `vfs_caches_init` → `rest_init`.
5. **`rest_init`**: creates `kernel_init` (PID 1) and `kthreadd` (PID 2) kernel threads; PID 1 is a kernel thread that becomes user-space init.
6. **`kernel_init`**: `initrd_load`, `prepare_namespace`, mounts real root, `run_init_process("/sbin/init")` — never returns.
7. **Init**: systemd reads units, starts `basic.target`, mounts, spawns services. Everything after is the normal OS.

## 10. Time Complexity
- Firmware POST: O(hardware init) — seconds to tens of seconds (server IPMI can be minutes).
- Bootloader: O(filesystem read) — fast.
- Kernel decompress: O(kernel size) — ~100ms-2s.
- `start_kernel` init: O(subsystems) — ~100ms-1s.
- systemd parallel service start: O(units) with parallelism — boot to login typically 3-30s (desktop), 10-60s+ (server with storage checks).
- Optimizations: kexec (skip firmware), resume-from-hibernation (restore memory image), fast boot via NVMe + parallel services.

## 11. Advantages
- **Modular**: firmware, bootloader, kernel, init each replaceable/upgradeable independently.
- **Secure**: signature verification per stage (Secure Boot, IMA, measured boot) blocks bootkits.
- **Flexible**: multi-OS (GRUB menu), kernel cmdline overrides, rescue modes.
- **Robust**: initramfs lets the kernel boot even when the root filesystem driver isn't compiled in.
- **Observable**: journalctl logs, `/proc/cmdline`, `efibootmgr` diagnostics.

## 12. Disadvantages
- **Long cold-boot times** (server POST can be minutes; firmware re-init is slow).
- **Complex failure chains**: a broken GRUB, missing initramfs, or bad root UUID stops boot with obscure errors.
- **Large trusted surface**: firmware itself is attackable (VulnUEFI, LogoFAIL — vulnerabilities in boot logos/parsers).
- **Brittleness in the wild**: Secure Boot key revocation breaks dual-boot; signed-module requirements complicate custom kernels.

## 13. Interview Questions
1. **Q: Walk through the boot process of a Linux machine.** A: Reset → UEFI/BIOS (POST, init, pick boot device) → bootloader (GRUB loads kernel + initramfs) → kernel decompress & `start_kernel()` → PID 1 (`systemd`/init) → services. 
2. **Q: What is the initramfs and why is it needed?** A: A minimal root filesystem image (cpio) loaded by the bootloader that provides early userspace with the drivers/scripts needed to find and mount the real root filesystem — the kernel doesn't yet know the root device.
3. **Q (TRICKY): What does `kexec` do and why would you use it?** A: `kexec` loads a new kernel into memory and jumps directly to it, skipping firmware/POST — used for fast reboot and hot kernel upgrades (also a reboot-path attack vector if compromised).
4. **Q: What is Secure Boot?** A: UEFI signature verification: firmware checks the bootloader's signature against enrolled db keys before executing it; the bootloader (e.g., `shim`+MOK) verifies the kernel. Prevents bootkits.
5. **Q: What's the difference between BIOS (legacy) and UEFI?** A: BIOS boots from a 512-byte MBR in 16-bit real mode; UEFI boots a PE executable from the ESP partition in 64-bit mode with services, Secure Boot, and a configurable boot manager (`efibootmgr`).
6. **Q: What is PID 1 and why is it special?** A: The first user-space process, spawned by `kernel_init`. It's the parent of all processes, is never killed (or it's "PID 1 zombie"), reaps orphans, and signals are handled specially (SIGKILL of PID 1 is ignored by the kernel).
7. **Q (PRODUCTION): Your server won't boot after a kernel update. How do you debug?** A: Check boot order/UEFI, boot an old kernel from GRUB, drop to a shell with `init=/bin/bash` or `rd.break`, inspect `journalctl -b -1`, check `/boot` space, verify grub.cfg and disk UUIDs.
8. **Q: What is POST?** A: Power-On Self-Test — firmware checks CPU, RAM, devices before boot; failures produce beep codes/diagnostics (and are why servers can hang minutes at boot).
9. **Q: What is hibernation and how does resume work?** A: The kernel writes RAM image to swap, then on resume it loads the image and restores state — boot effectively becomes "fast resume" (Windows Fast Startup / Linux `resume=`); firmware stages are skipped.
10. **Q (TRICKY): Can a root filesystem be mounted without initramfs?** A: Yes if the kernel has the filesystem + disk drivers built-in (no modules) — older kernels booted that way (`root=`, `rootwait`); initramfs exists to avoid bloating the kernel image with drivers.
11. **Q: What is GRUB's role in multiboot?** A: GRUB understands the multiboot spec and can boot Linux, Windows (via chainloading), BSD, and others from a common menu — it hides filesystem and firmware differences.
12. **Q: What is measured boot / TPM?** A: Firmware and bootloader record hashes (PCRs) of each stage into the TPM; later software (e.g., `tpm2-tools`, systemd) can attest that boot ran the expected components — the foundation of full-disk encryption keys (LUKS+TMP) and remote attestation.
13. **Q: What happens if the kernel panics during boot?** A: It prints a panic and halts/reboots (panic=1). Common causes: missing root device, corrupted initramfs, incompatible drivers, OOM during init — fixed via cmdline, older kernel, or initramfs repair.
14. **Q: What is `systemd` beyond "the init process"?** A: PID 1 that manages units (services, mounts, sockets), dependency graphs, parallel startup, cgroups for resource control, journald logging, and system states (targets) — the modern Linux init and service manager.
15. **Q (SCENARIO): Why does a server reboot faster with kexec-reboot than a normal reboot?** A: Normal reboot re-runs full firmware POST + init; kexec jumps straight to the new kernel in memory — seconds vs minutes on big servers. Clouds use this for kernel hot-swaps.

## 14. Follow-Up Questions
1. **Q: What is `shim`?** A: A small signed UEFI binary that validates and hands off to GRUB using Machine Owner Keys (MOK), so distro-signed GRUB can run under Secure Boot without the distro holding the platform keys.
2. **Q: What is the difference between initrd and initramfs?** A: initrd is a block-device-backed RAM disk; initramfs is a cpio archive unpacked into tmpfs — initramfs is smaller, kernel-native, and standard today.
3. **Q: What is `nomodeset` on the kernel cmdline?** A: Disables kernel mode-setting for the GPU, useful when a graphics driver hangs at boot.
4. **Q: What does `rootdelay=`/`rootwait` do?** A: Waits for the root device to appear (slow USB/RAID controllers); without it, the kernel may fail to find root and panic.
5. **Q: What is the difference between BIOS "MBR" boot and GPT?** A: MBR = 512-byte boot sector at LBA 0; GPT = modern partition table with ESP, CRC32, backup tables, plus UEFI firmware. Legacy BIOS can boot GPT with compatibility modes (hybrid MBR).

## 15. Coding Example
```bash
#!/bin/bash
# Inspecting the boot chain on a running Linux system
echo "== Current kernel command line =="
cat /proc/cmdline                      # e.g., BOOT_IMAGE=... root=... ro
echo "== UEFI boot entries =="
efibootmgr -v                          # BootOrder, Boot0000 entries
echo "== GRUB config used =="
grep -E "menuentry|linux|initrd" /boot/grub/grub.cfg | head -20
echo "== Last boot journal (errors) =="
journalctl -b -1 -p err --no-pager | tail -30
echo "== Kernel boot log =="
dmesg | grep -E "Kernel command line|Freeing unused|Run /sbin/init" | head
```
```pseudocode
# Boot trust/control chain
Reset vector
  -> UEFI firmware: POST, init, Secure Boot verify(bootloader)
  -> Bootloader (GRUB): find kernel+initramfs, build boot_params, ExitBootServices
  -> Kernel: decompress -> head_64.S -> start_kernel():
        setup_arch -> mm_init -> sched_init -> init_IRQ -> time_init -> rest_init
  -> PID 1 (kernel_init): mount root, run /sbin/init (systemd)
  -> systemd: targets -> services -> login
```

## 16. Industry Usage
- **Cloud providers**: AWS/Azure/GCP instances boot with UEFI/OVMF, network+image roots, cloud-init for config; kernel upgrades often via kexec or instance replacement.
- **Bare metal**: Dell/HP iDRAC/iLO console shows the full POST; fast-reboot and `kexec` used by orchestration.
- **Containers on bare metal**: microVMs (Firecracker, Kata) boot a minimal kernel in milliseconds using optimized boot paths — proving the boot chain can be radically shortened.
- **Secure enterprise**: Secure Boot + measured boot + TPM in Windows (BitLocker), macOS (Secure Enclave), and Linux (systemd-boot + LUKS-TPM).
- **Automotive/embedded**: boot in ms (flash loader → RTOS image) with no UEFI — a constrained version of the same chain.
- **Interview angle**: "server won't boot" troubleshooting, Secure Boot/TPM, PID 1 semantics, and kexec are hot FAANG SRE questions.

## 17. References
- UEFI Specification (uefi.org) — boot services, Secure Boot, ESP.
- Silberschatz, *OS Concepts*, Ch. 1.4 (Operating-System Structure) and 2.11 (Booting).
- Tanenbaum, *Modern OS*, Ch. 10.3 (Linux boot).
- Linux source: `init/main.c` (`start_kernel`), `arch/x86/boot/header.S`, `arch/x86/kernel/head_64.S`, `arch/x86/kernel/setup.c`.
- GRUB manual: gnu.org/software/grub/manual.
- Freedesktop: systemd boot/systemd manuals (systemd(1), systemd.special(7)).
- docs.kernel.org — "Linux kernel and booting" / initramfs docs.

## 18. Cheat Sheet
- Chain: Reset → UEFI/BIOS (POST) → Bootloader (GRUB) → Kernel (`start_kernel`) → PID 1 (systemd).
- initramfs = early userspace to find/mount real root.
- Secure Boot = per-stage signature verification vs bootkits.
- PID 1 = first process, orphan reaper, immune to SIGKILL.
- kexec = jump to new kernel, skip firmware.
- measured boot/TPM = PCR hashes for attestation + disk keys.
- BIOS legacy = MBR real-mode; UEFI = ESP PE executables.
- `root=`, `init=`, `nomodeset`, `rootwait` = common cmdline knobs.
- MicroVMs (Firecracker) boot kernels in ms.
- `journalctl -b -1` = previous boot's logs for debugging.

## 19. Quiz
1. The very first code to run is: a) kernel b) firmware c) systemd d) GRUB → **b**
2. Which verifies the bootloader in Secure Boot? a) kernel b) firmware c) systemd d) TPM only → **b**
3. initramfs is: a) a disk partition b) a cpio archive/tmpfs root c) firmware d) a bootloader → **b**
4. PID 1 is: a) kthreadd b) systemd/init c) bash d) the idle task → **b**
5. `kexec` skips: a) kernel init b) firmware/POST c) systemd d) mounting root → **b**
6. BIOS (legacy) boots from: a) ESP b) MBR sector 0 c) TPM d) NVMe only → **b**
7. Measured boot stores hashes in: a) /etc b) TPM PCRs c) EFI vars d) swap → **b**
8. MicroVM kernels (Firecracker) boot in: a) minutes b) milliseconds c) hours d) 30s+ → **b**
9. Which can rescue a boot with bad root fs? a) nomodeset b) init=/bin/bash c) kexec d) Secure Boot → **b**
10. `shim`'s job: a) load firmware b) let signed GRUB run under Secure Boot via MOK c) format disk d) encrypt root → **b**

## 20. Flashcards
- **Q: Boot chain order?** → **A:** Reset → UEFI/BIOS → bootloader → kernel → PID 1 (systemd).
- **Q: Why initramfs?** → **A:** Early userspace to find/mount the real root filesystem.
- **Q: Secure Boot does what?** → **A:** Verifies each boot stage's signature vs enrolled keys.
- **Q: What is PID 1?** → **A:** First user process, orphan reaper; SIGKILL-immune.
- **Q: kexec?** → **A:** Jump to new kernel in memory, skipping firmware.
- **Q: Measured boot?** → **A:** Hash each stage into TPM PCRs for attestation.
- **Q: UEFI vs BIOS?** → **A:** PE exe from ESP vs 512B MBR real-mode.
- **Q: How to debug a no-boot?** → **A:** GRUB old kernel, init=/bin/bash, journalctl -b -1, cmdline checks.

## 21. Revision
Booting is a staged trust handoff: reset → firmware (POST, Secure Boot, boot-device selection) → bootloader (GRUB loads kernel + initramfs) → kernel (`start_kernel`: arch, MM, scheduler, IRQ, VFS) → PID 1 (systemd). initramfs provides early userspace to mount the real root; kexec skips firmware for fast reboots; Secure Boot + measured boot/TPM protect against bootkits; PID 1 reaps orphans and resists SIGKILL. Debug no-boot with GRUB fallback, `init=/bin/bash`, `journalctl -b -1`. This chain is also why microVMs can boot in milliseconds.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Walk through booting" | 2 How It Works / 8 Example |
| "What is initramfs?" | 13 Q2 / 4 Why Not |
| "What is Secure Boot / TPM?" | 13 Q4, Q12 / 16 Industry Usage |
| "What is PID 1?" | 13 Q6 / 2 How It Works |
| "Debug a server that won't boot" | 13 Q7 / 16 Industry Usage |
| "kexec / fast reboot?" | 13 Q3, Q15 / 3 When Used |
| "BIOS vs UEFI?" | 13 Q5 / 4 Why Not |
| "Hibernation/fast startup?" | 13 Q9 / 3 When Used |
| "initrd vs initramfs / shim?" | 14 Follow-Up Q1-2 |
| "How do microVMs boot so fast?" | 16 Industry Usage |
