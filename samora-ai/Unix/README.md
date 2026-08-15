# Unix Interview Questions and Answers (Top 100)

## Q1: What is the Unix philosophy?
**A:** Write programs that do one thing well, work together via text streams, and avoid unnecessary output. Small composable tools connected by pipes are preferred over monolithic programs.

## Q2: What is the difference between the kernel and the shell?
**A:** The kernel is the core of the OS that manages hardware, memory, processes, and system calls. The shell is a command-line interpreter (user interface) that reads commands and invokes kernel services on the user's behalf.

## Q3: What is a shell in Unix?
**A:** A shell is a command-line interpreter that provides the user interface to the Unix kernel. Examples include sh, bash, ksh, csh, and zsh.

## Q4: Name the common Unix shells.
**A:** Bourne shell (sh), Bourne Again Shell (bash), Korn shell (ksh), C shell (csh), TC shell (tcsh), and Z shell (zsh).

## Q5: What is the difference between sh, bash, ksh, and csh?
**A:** sh is the original Bourne shell; bash is its GNU enhancement with job control and history; ksh adds scripting features; csh uses C-like syntax and is less ideal for scripting. bash is the most common default today.

## Q6: What is the purpose of the `ls` command?
**A:** It lists directory contents. Common flags: `ls -l` (long format), `ls -a` (including hidden), `ls -lh` (human-readable sizes).

## Q7: How do you change directories?
**A:** Use `cd`. `cd /path` moves to an absolute path; `cd ..` moves up one level; `cd` or `cd ~` returns to the home directory.

## Q8: What does `pwd` do?
**A:** It prints the absolute path of the current working directory.

## Q9: How do you copy files and directories?
**A:** Use `cp source dest`. Copy recursively with `cp -r dir1 dir2`. Preserve attributes with `cp -a`.

## Q10: How do you move or rename files?
**A:** Use `mv old new`. It renames within a filesystem or moves across directories; `mv a.txt b.txt` renames the file.

## Q11: How do you delete files and directories?
**A:** Use `rm file` to delete files and `rm -r dir` to delete directories recursively. Use `rm -f` to force without prompting.

## Q12: How do you create a directory?
**A:** Use `mkdir dirname`. Create nested directories with `mkdir -p a/b/c`.

## Q13: How do you remove an empty directory?
**A:** Use `rmdir dirname`. It only removes directories that contain no files or subdirectories.

## Q14: What does the `touch` command do?
**A:** It creates an empty file if it does not exist, or updates the access/modification timestamps of an existing file.

## Q15: How do you view file contents?
**A:** Use `cat` to print all, `less` for paginated viewing, `more` for basic paging. `less file` lets you scroll and search.

## Q16: What is the difference between `more` and `less`?
**A:** `more` allows forward-only paging; `less` allows both forward and backward scrolling, searching, and is generally more feature-rich.

## Q17: How do you view the first or last lines of a file?
**A:** Use `head -n 10 file` for the first 10 lines and `tail -n 10 file` for the last 10 lines. `tail -f file` follows appended data in real time.

## Q18: What does `tail -f` do?
**A:** It outputs the last lines and keeps the file open, displaying new lines as they are appended—useful for monitoring logs.

## Q19: What does the `wc` command do?
**A:** It counts lines, words, and bytes. `wc -l` counts lines, `wc -w` words, `wc -c` bytes.

## Q20: What is the Unix file system hierarchy (FHS)?
**A:** A tree rooted at `/` where `/bin` holds binaries, `/etc` config, `/home` user homes, `/var` variable data, `/tmp` temp files, `/usr` user programs, `/dev` devices, `/proc` process info.

## Q21: What is the root directory?
**A:** The top of the filesystem tree, denoted `/`, from which all other files and directories branch.

## Q22: What is the purpose of `/etc`, `/var`, `/tmp`, `/usr`?
**A:** `/etc` stores system configuration files; `/var` holds variable data like logs and spools; `/tmp` is for temporary files; `/usr` contains user-installed software and shareable read-only data.

## Q23: What is an inode?
**A:** An inode is a data structure storing metadata about a file (permissions, ownership, size, timestamps, data block pointers) but not its name. Each file has a unique inode number on a filesystem.

## Q24: What is the difference between a hard link and a soft (symbolic) link?
**A:** A hard link shares the same inode and data; deleting the original keeps data. A soft link (`ln -s`) points to a path name and breaks if the target is removed.

## Q25: How do you create a symbolic link?
**A:** Use `ln -s target linkname`. Example: `ln -s /var/www/html site`.

## Q26: What are the different file types in Unix?
**A:** Regular files (`-`), directories (`d`), symbolic links (`l`), character devices (`c`), block devices (`b`), pipes (`p`), and sockets (`s`), shown by the first character of `ls -l`.

## Q27: How do you change file permissions?
**A:** Use `chmod`. Symbolic: `chmod u+x file`; numeric: `chmod 755 file` (rwxr-xr-x).

## Q28: Explain numeric (octal) permission notation.
**A:** Each digit is r=4, w=2, x=1 summed per class. `chmod 750` means owner rwx (7), group r-x (5), others none (0).

## Q29: Explain symbolic permission notation.
**A:** Format `who(op)(perm)` where who is u/g/o/a, op is +/-/=, perm is r/w/x. Example: `chmod g-w file` removes group write.

## Q30: What does `chown` do?
**A:** It changes file ownership. `chown user:group file` sets owner and group; `chown -R` recurses.

## Q31: What does `chgrp` do?
**A:** It changes the group ownership of a file or directory. `chgrp staff file`.

## Q32: What is umask?
**A:** It sets the default permission mask for newly created files. A umask of `022` yields files `644` and dirs `755`.

## Q33: What are the SUID, SGID, and sticky bits?
**A:** SUID (`4000`) runs a program with the file owner's privileges; SGID (`2000`) runs with the group's privileges or inherits group on dirs; sticky bit (`1000`) on a dir lets only owners delete their own files (e.g., `/tmp`).

## Q34: How do you set the SUID bit?
**A:** `chmod u+s file` or `chmod 4755 file`. The permission shows `s` in the owner execute position.

## Q35: What is the default umask for most systems and why?
**A:** Typically `022`, producing files `644` (rw-r--r--) so new files are not world-writable by default.

## Q36: How do you view running processes?
**A:** Use `ps` (snapshot), `ps aux` for all processes, or `top`/`htop` for a live, sortable view.

## Q37: What does `top` display?
**A:** A real-time, updating list of processes with CPU, memory usage, load averages, and process statistics.

## Q38: How do you kill a process?
**A:** Use `kill PID` to send SIGTERM; `kill -9 PID` sends SIGKILL to force termination. `pkill name` kills by name.

## Q39: What is the difference between `kill` and `kill -9`?
**A:** `kill` (SIGTERM, 15) requests graceful exit, allowing cleanup. `kill -9` (SIGKILL) cannot be caught or ignored and forcibly stops the process.

## Q40: What are Unix signals? Name a few.
**A:** Signals notify processes of events. Common ones: SIGHUP (1), SIGINT (2, Ctrl+C), SIGTERM (15), SIGKILL (9), SIGSTOP (19), SIGCONT (18).

## Q41: What does `Ctrl+C` and `Ctrl+Z` do?
**A:** `Ctrl+C` sends SIGINT to terminate the foreground process; `Ctrl+Z` sends SIGTSTP to suspend it to the background.

## Q42: What are `nice` and `renice`?
**A:** `nice` launches a process with adjusted scheduling priority (range -20 to 19, lower = higher priority). `renice` changes priority of a running process.

## Q43: How do you run a command in the background?
**A:** Append `&`: `long_task &`. Use `jobs` to list, `fg` to bring to foreground, `bg` to resume in background.

## Q44: What is the difference between `jobs`, `fg`, and `bg`?
**A:** `jobs` lists background/suspended tasks of the current shell; `fg %n` brings job n to foreground; `bg %n` resumes a suspended job in the background.

## Q45: What does `nohup` do?
**A:** It runs a command immune to hangups (SIGHUP) so it keeps running after the shell/logout. Output goes to `nohup.out` unless redirected.

## Q46: What is a pipe in Unix?
**A:** A pipe (`|`) connects stdout of one command to stdin of the next, enabling composition. `cat file | grep err | wc -l`.

## Q47: Explain standard input, output, and error.
**A:** stdin (fd 0) is input, stdout (fd 1) is normal output, stderr (fd 2) is error output. They can be redirected independently.

## Q48: How do you redirect output to a file?
**A:** `>` overwrites, `>>` appends. `command > out.txt 2>&1` redirects both stdout and stderr.

## Q49: How do you redirect stderr only?
**A:** `command 2> errors.txt`. To append: `command 2>> errors.txt`.

## Q50: What does the `tee` command do?
**A:** It reads stdin and writes to both stdout and one or more files. `command | tee result.txt` displays and saves output.

## Q51: What is `grep` and how is it used?
**A:** `grep` searches text for a pattern. `grep "error" log.txt` prints matching lines; `-i` ignores case, `-r` recurses, `-v` inverts.

## Q52: Difference between `grep`, `egrep`, and `fgrep`?
**A:** `egrep` (or `grep -E`) supports extended regex; `fgrep` (or `grep -F`) treats patterns as fixed strings (no regex); `grep` uses basic regex.

## Q53: How do you count lines matching a pattern?
**A:** `grep -c "pattern" file` counts matching lines. Combine with `wc -l` as an alternative.

## Q54: What is `sed`?
**A:** A stream editor for filtering and transforming text via scripts. `sed 's/foo/bar/g' file` replaces foo with bar globally.

## Q55: Give a `sed` substitution example.
**A:** `sed 's/old/new/g' input.txt > output.txt` replaces all occurrences of "old" with "new".

## Q56: What is `awk`?
**A:** A pattern-scanning and processing language, great for columnar data. `awk '{print $1, $3}' file` prints the first and third fields (default whitespace-delimited).

## Q57: How do you sum a numeric column with `awk`?
**A:** `awk '{sum+=$1} END {print sum}' file` accumulates the first column and prints the total at the end.

## Q58: What does the `find` command do?
**A:** It searches the filesystem for files by name, type, size, time, permissions. `find /var -name "*.log" -mtime +7`.

## Q59: How do you find files modified in the last 7 days?
**A:** `find . -type f -mtime -7` lists files modified within the last 7 days.

## Q60: What is `locate` and how does it differ from `find`?
**A:** `locate` searches a prebuilt database (fast) for filenames, while `find` walks the directory tree live (slower but accurate). Update the DB with `updatedb`.

## Q61: How do you archive files with `tar`?
**A:** `tar -cvf archive.tar dir/` creates an archive; `tar -xvf archive.tar` extracts; `-z` adds gzip, `-j` adds bzip2.

## Q62: How do you compress files with `gzip` and `bzip2`?
**A:** `gzip file` produces `file.gz`; `bzip2 file` produces `file.bz2`. Decompress with `gunzip`/`bunzip2`. They compress single files (use with tar for directories).

## Q63: How do you create and extract a zip archive?
**A:** `zip -r archive.zip dir/` creates; `unzip archive.zip` extracts. Zip compresses and archives together.

## Q64: What is `cron` and how do you use it?
**A:** `cron` runs scheduled jobs via crontab. `crontab -e` edits; the format is `min hour dom month dow command`.

## Q65: Explain the crontab time format.
**A:** Five fields: minute (0-59), hour (0-23), day-of-month (1-31), month (1-12), day-of-week (0-7). `0 2 * * *` runs at 2am daily.

## Q66: How do you list and remove cron jobs?
**A:** `crontab -l` lists your jobs; `crontab -r` removes all; `crontab -e` edits them.

## Q67: What is the `at` command?
**A:** It schedules a one-time job at a specified time. `echo "backup.sh" | at 23:00` runs the command tonight at 11pm.

## Q68: What are environment variables?
**A:** Name-value pairs available to processes that affect behavior. Set with `VAR=value` and export with `export VAR`. View with `env` or `printenv`.

## Q69: What is the `PATH` variable?
**A:** A colon-separated list of directories the shell searches for executables. `echo $PATH`; add with `export PATH=$PATH:/new/dir`.

## Q70: What is the `HOME` variable and how do you set environment variables persistently?
**A:** `HOME` is the user's home directory. To persist, add exports to `~/.bashrc` or `~/.profile`.

## Q71: How do you display the value of a variable?
**A:** Prefix with `$`: `echo $HOME`. Use `set` to see shell variables and `env` for environment variables.

## Q72: What is the difference between a shell variable and an environment variable?
**A:** Shell variables are local to the shell session; environment variables are exported and inherited by child processes via `export`.

## Q73: What is `cut` used for?
**A:** It extracts columns or character ranges. `cut -d: -f1 /etc/passwd` prints the first field (username) using `:` as delimiter.

## Q74: What does `sort` do and how do you sort numerically?
**A:** It orders lines. `sort file` lexically; `sort -n` numerically; `sort -r` reverse; `sort -k2` by column 2.

## Q75: What does `uniq` do?
**A:** It removes or reports adjacent duplicate lines. Usually paired with `sort`: `sort file | uniq`. Use `-c` to count, `-d` to show duplicates.

## Q76: What is `tr` used for?
**A:** It translates or deletes characters. `tr 'a-z' 'A-Z' < file` uppercases; `tr -d '\r'` deletes carriage returns.

## Q77: What do `paste`, `join`, `comm`, and `diff` do?
**A:** `paste` merges lines side-by-side; `join` joins on a common field; `comm` compares sorted files by lines; `diff` shows line differences between files.

## Q78: How do you create a patch with `diff`?
**A:** `diff -u old.txt new.txt > fix.patch` creates a unified diff; apply with `patch old.txt < fix.patch`.

## Q79: What are regular expressions in Unix?
**A:** Patterns describing text. `.` matches any char, `*` repeats previous, `^` start, `$` end, `[...]` class, `\` escapes. Used by grep, sed, awk.

## Q80: What is the difference between basic and extended regex?
**A:** Basic regex (grep) requires escaping for `+`, `?`, `()`, `{}`. Extended regex (egrep/grep -E) uses them unescaped.

## Q81: How do you start and exit the `vi` editor?
**A:** `vi file` opens; press `i` to insert, `Esc` to command mode, `:w` to save, `:q` to quit, `:wq` save and quit, `:q!` quit without saving.

## Q82: Name a few essential `vi` commands.
**A:** `dd` deletes a line, `yy` yanks, `p` pastes, `/pattern` searches, `:s/old/new/g` substitutes, `G` goes to end, `0` start of line.

## Q83: What is a shell script and how do you run one?
**A:** A file of shell commands. Make it executable with `chmod +x script.sh` and run `./script.sh`, or `bash script.sh`.

## Q84: How do you make a script executable?
**A:** `chmod +x script.sh` then run it with `./script.sh`. A shebang (`#!/bin/bash`) on the first line defines the interpreter.

## Q85: What is a shebang line?
**A:** The first line `#!/path/interpreter` tells the kernel which program executes the script, e.g., `#!/bin/bash`.

## Q86: How do you mount and unmount a filesystem?
**A:** `mount /dev/sdb1 /mnt/usb` mounts; `umount /mnt/usb` unmounts. Always unmount before removing removable media.

## Q87: What do `df` and `du` report?
**A:** `df` shows disk space used/free per mounted filesystem; `du` shows directory/file space usage, e.g., `du -sh dir`.

## Q88: How do you check memory usage?
**A:** `free -h` shows RAM and swap; `top`/`htop` also display memory. `vmstat` gives a broader view.

## Q89: How do you check disk usage of a directory?
**A:** `du -sh /path` gives a human-readable total; `du -h --max-depth=1 /path` lists subdirectory sizes.

## Q90: How do you add a user?
**A:** `useradd -m username` creates the user with a home dir; set password with `passwd username`. On some systems `adduser` is interactive.

## Q91: How do you change a user's password?
**A:** `passwd username` (root) or just `passwd` for the current user prompts for a new password.

## Q92: What does `groups` show and what is `sudo`?
**A:** `groups` lists a user's group memberships. `sudo` runs a command as another user (default root) per `/etc/sudoers`.

## Q93: What is the difference between `su` and `sudo`?
**A:** `su` switches to another user (needs their password, root by default); `sudo` runs a single command as root using the invoking user's password and is logged.

## Q94: What are basic networking commands?
**A:** `ping` tests connectivity; `ip a`/`ifconfig` shows interfaces; `netstat -tulpn` lists listening ports; `nc` (netcat) for raw TCP/UDP; `telnet host port` tests a port.

## Q95: How do you check listening ports and interfaces?
**A:** `netstat -tulpn` or `ss -tulpn` shows listening sockets; `ip addr` (or `ifconfig`) shows network interfaces and IPs.

## Q96: What is the difference between `ifconfig` and `ip`?
**A:** `ifconfig` is the legacy BSD tool; `ip` (from iproute2) is the modern replacement for managing interfaces, routes, and addresses.

## Q97: What is inter-process communication (IPC) in Unix?
**A:** Mechanisms for processes to exchange data: pipes, named pipes (FIFOs), signals, shared memory, message queues, semaphores, and sockets.

## Q98: What is the difference between a system call and a library call?
**A:** A system call is a request to the kernel (e.g., `open`, `read`); a library call is a function in a user-space library (e.g., `printf`), which may internally invoke syscalls.

## Q99: Describe the Unix boot process and runlevels/init.
**A:** BIOS/UEFI boots, loads the bootloader (GRUB), which loads the kernel and initial RAM disk. The kernel starts `init` (or systemd), which brings the system to a runlevel/target. System V had runlevels 0-6; systemd uses targets like `multi-user.target`.

## Q100: What is the difference between Unix and Linux, and BSD vs System V?
**A:** Unix is the original OS family (trademarked); Linux is a Unix-like kernel. BSD (Berkeley) and System V (AT&T) are Unix lineages differing in init, printing, and commands; Linux blends both, with GNU userland. Best practice: script portably with POSIX `sh` and avoid GNU-only flags when cross-platform compatibility matters.
