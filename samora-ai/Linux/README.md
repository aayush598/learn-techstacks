# Linux Interview Questions and Answers (Top 100)

## Q1: What is Linux and how does it differ from Unix?
**A:** Linux is an open-source, Unix-like operating system kernel created by Linus Torvalds. Unlike traditional Unix (e.g., AIX, Solaris, HP-UX), Linux is free, community/ commercially supported, and runs on virtually any hardware architecture.

## Q2: What are the main components of a Linux system?
**A:** The kernel (core resource manager), the shell (command interpreter), system libraries (glibc), and system utilities/applications. The kernel manages processes, memory, devices, and the filesystem.

## Q3: What is the Linux kernel and what does it do?
**A:** The kernel is the core of the OS that abstracts hardware and manages CPU, memory, I/O, and processes. You can check its version with:
```bash
uname -r
```

## Q4: What is a Linux distribution?
**A:** A distro bundles the Linux kernel with package managers, desktop environments, and default configs. Examples include Ubuntu, Debian, RHEL, CentOS, Fedora, and Arch.

## Q5: Name a few differences between Debian/Ubuntu and RHEL/CentOS families.
**A:** Debian/Ubuntu use `.deb` packages with `apt`/`dpkg`, while RHEL/CentOS use `.rpm` packages with `yum`/`dnf`/`rpm`. They also differ in init defaults (both use systemd now), release cadence, and support models.

## Q6: What package manager does Debian/Ubuntu use?
**A:** `apt` (and the lower-level `apt-get`/`dpkg`) manages `.deb` packages and dependencies:
```bash
sudo apt update
sudo apt install nginx
```

## Q7: What is the difference between apt and apt-get?
**A:** `apt` is a modern, user-friendly CLI combining common `apt-get`/`apt-cache` functions with nicer output. `apt-get` is script-oriented and stable for automation; both manage the same underlying package database.

## Q8: How do you install a .deb file manually?
**A:** Use `dpkg` for local install, then fix dependencies with `apt`:
```bash
sudo dpkg -i package.deb
sudo apt -f install
```

## Q9: How do you remove a package with apt?
**A:** `sudo apt remove pkg` keeps config files; `sudo apt purge pkg` removes configs too. Add `--auto-remove` to delete unused dependencies.

## Q10: What package managers are used on RHEL/CentOS/Fedora?
**A:** Older RHEL/CentOS use `yum`; modern Fedora/RHEL 8+ use `dnf`. Both resolve dependencies from RPM repositories:
```bash
sudo dnf install httpd
```

## Q11: How do you install a .rpm package?
**A:** Use `rpm` directly or `dnf`/`yum` for dependency resolution:
```bash
sudo rpm -ivh package.rpm
sudo dnf install ./package.rpm
```

## Q12: What does `rpm -qa` do?
**A:** It queries and lists all installed RPM packages. Pipe to `grep` to find a specific package:
```bash
rpm -qa | grep nginx
```

## Q13: What are snap and flatpak?
**A:** Both are universal, distro-independent packaging formats that bundle apps with dependencies. Snaps (Canonical) are common on Ubuntu; Flatpak (Red Hat/Freedesktop) is popular on Fedora/desktop Linux.

## Q14: How do you list installed snaps?
**A:** Use the `snap` command:
```bash
snap list
sudo snap install code --classic
```

## Q15: How do you update all packages on Ubuntu vs RHEL?
**A:** Ubuntu: `sudo apt update && sudo apt upgrade -y`. RHEL/Fedora: `sudo dnf upgrade -y` (or `sudo yum update -y` on older systems).

## Q16: Describe the Linux boot process.
**A:** BIOS/UEFI → bootloader (GRUB) → kernel loads → initramfs mounts root → kernel starts the init process (systemd as PID 1) → default target/runlevel starts services.

## Q17: What is GRUB?
**A:** GRUB (GRand Unified Bootloader) is the default Linux bootloader that loads the kernel and initramfs and lets you choose kernels or pass boot parameters. Its config is `/boot/grub/grub.cfg`, generated from `/etc/default/grub`.

## Q18: How do you update the GRUB configuration?
**A:** Edit `/etc/default/grub` then regenerate:
```bash
sudo update-grub          # Debian/Ubuntu
sudo grub2-mkconfig -o /boot/grub2/grub.cfg   # RHEL/CentOS
```

## Q19: What is initramfs?
**A:** An initial RAM filesystem loaded by the kernel at boot containing drivers/modules needed to mount the real root filesystem (e.g., disk controllers, LVM, RAID).

## Q20: How can you boot into a single-user / rescue mode?
**A:** At the GRUB menu, edit the kernel line adding `single` or `systemd.unit=rescue.target`, or select "Recovery Mode" on Ubuntu to get a root shell for repairs.

## Q21: What is systemd?
**A:** systemd is the modern init system and service manager (PID 1) that parallelizes boot, manages services, mounts, devices, and logs via journald.

## Q22: What is the difference between systemd and SysVinit?
**A:** SysVinit uses sequential runlevel scripts in `/etc/init.d` and is slow; systemd uses unit files, parallel startup, dependency-based activation, and centralized logging.

## Q23: How do you start, stop, enable, and check a service with systemctl?
**A:**
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
sudo systemctl is-enabled nginx
```

## Q24: What are systemd units?
**A:** Configuration files describing resources systemd manages: `.service`, `.target`, `.socket`, `.mount`, `.timer`, `.device`. They live in `/etc/systemd/system` (admin) and `/lib/systemd/system` (packages).

## Q25: What are systemd targets?
**A:** Targets are synchronization points grouping units, replacing SysV runlevels. Common ones: `multi-user.target` (CLI), `graphical.target` (GUI), `rescue.target`, `poweroff.target`.

## Q26: How do you change the default boot target?
**A:**
```bash
sudo systemctl set-default multi-user.target
sudo systemctl get-default
```

## Q27: How do you view logs with journalctl?
**A:**
```bash
journalctl -u nginx -f      # follow a service
journalctl --since "2026-01-01" --until "2026-01-02"
journalctl -p err -b        # errors since last boot
```

## Q28: How do you reboot or power off using systemd?
**A:** `sudo systemctl reboot`, `sudo systemctl poweroff`, or `sudo shutdown -h now`. `shutdown` is a compatibility wrapper.

## Q29: What is a systemd timer and how does it differ from cron?
**A:** A `.timer` unit triggers a `.service` at specified times/conditions with better logging and dependency handling. It's systemd's replacement for some cron jobs.

## Q30: How do you mask a service so it cannot be started?
**A:** `sudo systemctl mask nginx` symlinks the unit to `/dev/null`, preventing accidental or dependency-based starts. Use `unmask` to revert.

## Q31: What is a daemon?
**A:** A daemon is a background process that runs without a controlling terminal, typically providing services (e.g., `sshd`, `nginx`). They are often named with a trailing `d`.

## Q32: How do you list all running services?
**A:**
```bash
systemctl list-units --type=service --state=running
```

## Q33: How do you view failed services?
**A:** `systemctl --failed` lists units that failed to start, useful for boot troubleshooting.

## Q34: What is the difference between a service being enabled and active?
**A:** `enabled` means it starts at boot; `active` (running) means it is currently running. A service can be enabled but inactive (stopped).

## Q35: How do you reload a service configuration without restarting?
**A:** `sudo systemctl reload nginx` (if supported) sends SIGHUP; otherwise `sudo systemctl restart nginx` to fully restart.

## Q36: How do you list running processes?
**A:**
```bash
ps aux          # all processes, BSD style
ps -ef          # all processes, standard style
```

## Q37: What does the `top` command show?
**A:** A real-time, interactive view of CPU, memory usage, load average, and per-process resource consumption. Press `q` to quit, `k` to kill, `1` to show per-core CPU.

## Q38: What is `htop` and how does it differ from top?
**A:** `htop` is an enhanced, colorful, scrollable process viewer with mouse support and easier kill/renice. It's usually installed separately (`apt install htop`).

## Q39: How do you kill a process by PID?
**A:**
```bash
kill 1234          # SIGTERM (graceful)
kill -9 1234       # SIGKILL (force)
```

## Q40: How do you kill processes by name?
**A:**
```bash
pkill nginx
killall firefox
```

## Q41: What is the difference between SIGTERM and SIGKILL?
**A:** SIGTERM (15) asks a process to shut down gracefully, allowing cleanup; SIGKILL (9) forcibly terminates it immediately with no cleanup, risking data loss.

## Q42: How do you find the PID of a process?
**A:**
```bash
pgrep nginx
pidof sshd
ps aux | grep apache2
```

## Q43: What is `nice` and `renice`?
**A:** `nice` sets a process's scheduling priority (range -20 to 19, lower = higher priority) at launch; `renice` changes it for a running process:
```bash
nice -n 10 tar czf backup.tgz /data
renice -n 5 -p 1234
```

## Q44: What does `strace` do?
**A:** It traces system calls and signals made by a process, invaluable for debugging:
```bash
strace -p 1234
strace -f -o out.txt ls
```

## Q45: What does `lsof` do?
**A:** Lists open files and the processes using them (everything is a file in Linux, including sockets):
```bash
lsof -i :80          # who is using port 80
lsof /var/log/syslog
```

## Q46: How do you find which process is using a port?
**A:**
```bash
ss -tlnp | grep :8080
lsof -i :8080
fuser 80/tcp
```

## Q47: How do you monitor a process's resource usage over time?
**A:** Use `top`/`htop` interactively, or `pidstat 1` (from `sysstat`) for per-PID CPU/memory sampling.

## Q48: What is a zombie process?
**A:** A process that has finished executing but still has an entry in the process table because its parent hasn't read its exit status via `wait()`. They consume no CPU/RAM but can exhaust PIDs; killing the parent usually clears them.

## Q49: How do you send a signal to all processes in a group?
**A:** Use `kill` with a negative PID (the group leader): `kill -TERM -1234`. This signals the whole process group.

## Q50: What does `nohup` do?
**A:** Runs a command immune to hangups/SIGHUP so it keeps running after the shell/terminal closes, typically with output redirected:
```bash
nohup ./longrun.sh > out.log 2>&1 &
```

## Q51: How do you check memory usage?
**A:**
```bash
free -h
cat /proc/meminfo
```

## Q52: What does `vmstat` report?
**A:** Virtual memory statistics: processes, memory, swap, IO, and CPU over time:
```bash
vmstat 1 5        # 5 samples, 1s apart
```

## Q53: What does `iostat` show?
**A:** CPU utilization and device I/O statistics (throughput, await, utilization). From the `sysstat` package:
```bash
iostat -xz 1
```

## Q54: What does `mpstat` show?
**A:** Per-processor CPU statistics, useful for spotting single-core bottlenecks:
```bash
mpstat -P ALL 1
```

## Q55: How do you check CPU info?
**A:**
```bash
lscpu
nproc              # number of CPUs
cat /proc/cpuinfo
```

## Q56: What is load average?
**A:** The average number of runnable + uninterruptible processes over 1, 5, and 15 minutes (shown by `uptime`/`top`). A value near the CPU core count indicates saturation.

## Q57: How do you check overall system performance quickly?
**A:** `top` for live view, `vmstat 1` for resource breakdown, and `sar` (from `sysstat`) for historical data collected periodically.

## Q58: What is the difference between buffer and cache memory?
**A:** Buffers hold data in transit to disk; cache holds recently read file data for fast reuse. Both are reclaimable, so "available" memory (`free -h`) is the truer free amount.

## Q59: How do you list block devices and disks?
**A:**
```bash
lsblk
fdisk -l
```

## Q60: How do you partition a disk?
**A:** Use `fdisk` for MBR or `parted` for GPT/larger disks:
```bash
sudo fdisk /dev/sdb
sudo parted /dev/sdb mklabel gpt mkpart primary ext4 0% 100%
```

## Q61: How do you create a filesystem?
**A:**
```bash
sudo mkfs.ext4 /dev/sdb1
sudo mkfs.xfs /dev/sdb1
```

## Q62: How do you mount a filesystem?
**A:**
```bash
sudo mount /dev/sdb1 /mnt/data
```

## Q63: How do you make a mount persistent?
**A:** Add an entry to `/etc/fstab` using the device, UUID, or label:
```bash
UUID=xxxx /mnt/data ext4 defaults 0 2
```
Get the UUID with `blkid`.

## Q64: How do you check disk space usage?
**A:**
```bash
df -h             # filesystem usage
du -sh /var/log   # directory size
```

## Q65: What does `blkid` do?
**A:** Prints block device attributes such as UUID and filesystem type, commonly used to populate `/etc/fstab` consistently across reboots.

## Q66: How do you unmount a filesystem?
**A:**
```bash
sudo umount /mnt/data
sudo umount /dev/sdb1
```
Use `umount -l` (lazy) if busy.

## Q67: How do you find what is using a mounted directory so you can unmount it?
**A:** `lsof +D /mnt/data` or `fuser -mv /mnt/data` to identify processes blocking the unmount.

## Q68: What is the purpose of `/etc/fstab`?
**A:** It defines static filesystem mounts applied at boot, with fields: device, mountpoint, type, options, dump, and fsck order. Errors here can prevent booting.

## Q69: How do you check and repair a filesystem?
**A:** `fsck` checks/repairs unmounted filesystems:
```bash
sudo fsck -y /dev/sdb1
```
For ext4 use `e2fsck`; never run on a mounted filesystem.

## Q70: What is LVM and what are its benefits?
**A:** Logical Volume Manager abstracts physical disks into volume groups and logical volumes, allowing flexible resizing, snapshots, and striping/mirroring without repartitioning.

## Q71: What are the basic LVM components?
**A:** PV (Physical Volume, a disk/partition), VG (Volume Group, pool of PVs), LV (Logical Volume, carved from a VG and formatted like a partition).

## Q72: How do you extend an LVM logical volume?
**A:**
```bash
sudo lvextend -L +10G /dev/vg0/lv_data
sudo resize2fs /dev/vg0/lv_data      # ext4
# or xfs_growfs /mountpoint for XFS
```

## Q73: How do you change file permissions with chmod?
**A:**
```bash
chmod 755 script.sh     # rwxr-xr-x
chmod u+x file          # add execute for owner
```
Numeric: r=4, w=2, x=1.

## Q74: What do the permission bits rwx mean for a directory?
**A:** `r` lets you list entries, `w` lets you create/delete files, `x` (execute) lets you `cd` into and traverse it. Without `x`, `r` is largely useless.

## Q75: How do you change ownership with chown?
**A:**
```bash
sudo chown user:group file
sudo chown -R www-data:www-data /var/www
```

## Q76: What is umask?
**A:** A default permission mask (e.g., `022`) subtracted from `666`/`777` when creating files/dirs, controlling default access. Set per-session via `umask 027`.

## Q77: What are special permission bits SUID, SGID, and sticky?
**A:** SUID (4) runs a file as its owner; SGID (2) runs as its group or sets group on new files in a dir; sticky (1, e.g., `/tmp`) lets only owners delete their own files. Set via `chmod 4755`, `chmod g+s`, `chmod +t`.

## Q78: How do you set an SUID bit?
**A:**
```bash
chmod u+s /usr/bin/passwd
chmod 4755 /usr/bin/passwd
```
Shown as `s` in the owner execute position (`-rwsr-xr-x`).

## Q79: What are ACLs and how do you use them?
**A:** Access Control Lists give per-user/group permissions beyond the standard owner/group/other model:
```bash
setfacl -m u:alice:rwx file
getfacl file
```

## Q80: How do you remove an ACL?
**A:**
```bash
setfacl -x u:alice file
setfacl -b file          # remove all ACLs
```

## Q81: How do you make a file immutable (even for root)?
**A:** Use `chattr` to set the immutable bit:
```bash
sudo chattr +i important.txt
sudo chattr -i important.txt   # to remove
```
List with `lsattr`.

## Q82: What is the difference between symbolic and numeric chmod?
**A:** Numeric uses octal (e.g., `644`); symbolic uses letters (`u`,`g`,`o`,`a` with `+`,`-`,`=`) which is relative and easier for targeted changes. Both edit the same permission bits.

## Q83: What is in /etc/passwd?
**A:** User account info (one line per user): `username:x:UID:GID:comment:home:shell`. The `x` means the password is in `/etc/shadow`.

## Q84: What is in /etc/shadow?
**A:** Secure user password hashes plus aging info (last change, min/max expiry, warning, inactivity). Readable only by root.

## Q85: What is in /etc/group?
**A:** Group definitions: `groupname:x:GID:member1,member2` listing groups and their members.

## Q86: How do you create a user?
**A:**
```bash
sudo useradd -m -s /bin/bash alice
sudo passwd alice
```
On Debian, `adduser` is a friendlier interactive wrapper.

## Q87: How do you modify a user (e.g., add to a group)?
**A:**
```bash
sudo usermod -aG docker alice
sudo usermod -s /bin/zsh alice
```
Always use `-a` (append) with `-G` to avoid removing existing groups.

## Q88: How do you delete a user?
**A:**
```bash
sudo userdel alice
sudo userdel -r alice     # also remove home dir
```

## Q89: How does sudo and /etc/sudoers work?
**A:** `/etc/sudoers` (edit with `visudo`) grants users/commands elevated privileges. Add `alice ALL=(ALL) NOPASSWD: /bin/systemctl restart nginx` for scoped, passwordless access.

## Q90: How do you switch users?
**A:**
```bash
su - alice        # login shell, loads env
sudo -i           # root login shell
sudo -u alice whoami
```

## Q91: How do you configure a static IP on modern Linux?
**A:** With NetworkManager via `nmcli`:
```bash
sudo nmcli con mod eth0 ipv4.method manual ipv4.addresses 192.168.1.10/24 ipv4.gateway 192.168.1.1
sudo nmcli con up eth0
```

## Q92: How do you view network interfaces and IP addresses?
**A:**
```bash
ip addr show
ip -br addr
ip link
```

## Q93: How do you check listening ports and connections?
**A:**
```bash
ss -tulnp
# legacy: netstat -tulnp
```

## Q94: How do you test connectivity and trace a route?
**A:**
```bash
ping -c 4 8.8.8.8
traceroute google.com
mtr google.com     # continuous trace
```

## Q95: How do you download files from the command line?
**A:**
```bash
curl -O https://example.com/file.tar.gz
wget https://example.com/file.tar.gz
```

## Q96: How do you configure a firewall with ufw?
**A:**
```bash
sudo ufw allow 22/tcp
sudo ufw enable
sudo ufw status
```
`ufw` is the simple frontend for Ubuntu; `firewalld` is used on RHEL.

## Q97: What is the difference between iptables and nftables?
**A:** `iptables` is the legacy packet-filtering framework; `nftables` is its successor offering a single unified framework, better performance, and simpler syntax (`nft` command). Modern distros default to nftables under firewalld.

## Q98: How do you manage firewalld?
**A:**
```bash
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
```

## Q99: How do you set up SSH key-based authentication?
**A:**
```bash
ssh-keygen -t ed25519
ssh-copy-id user@host
```
Then disable password auth in `/etc/ssh/sshd_config` (`PasswordAuthentication no`) and reload `sshd`.

## Q100: How do you create an SSH tunnel / port forward?
**A:** Local forward: `ssh -L 8080:localhost:80 user@host` (access remote port 80 via local 8080). Remote forward: `ssh -R 9000:localhost:3000 user@host`. Use `-N` to avoid a shell and `-f` to background it.
