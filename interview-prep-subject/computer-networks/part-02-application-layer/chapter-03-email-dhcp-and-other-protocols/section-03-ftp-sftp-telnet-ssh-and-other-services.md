# FTP, SFTP, Telnet, SSH, and Other Services

> **TL;DR**: The classic session/file protocols — **FTP** (port 21 control + data), **SFTP/SCP** (SSH-based file transfer, port 22), **Telnet** (port 23, plaintext remote shell), and **SSH** (port 22, encrypted remote shell) — exist to move files and run commands remotely, and the history is a security story: insecure plaintext (FTP, Telnet) gave way to encrypted replacements (FTPS/SFTP, SSH).

## 1. Why Does This Exist?
Two eternal needs: **move files between machines** and **operate a machine remotely**. Early networks (ARPANET) needed both, so FTP (1971, RFC 114→959) and Telnet (1969, RFC 15→854) were built. They worked — but with *zero* security: FTP sends passwords in plaintext and Telnet transmits everything (including root passwords) unencrypted. As the Internet became hostile, encrypted successors arose: **SSH** (1995, RFC 4251) replaced Telnet for remote shell and became the secure-transport of choice for **SFTP** (SSH File Transfer Protocol) and **SCP**; **FTPS** (FTP over TLS) kept FTP's model but added encryption. Today the group answers: "how do engineers manage servers, deploy code, and move data securely?"

## 2. How Does It Work?
- **FTP** (RFC 959): a *control connection* (port **21**, text commands USER/PASS/LIST/STOR/RETR) plus a separate *data connection* for actual file bytes. Two modes:
  - **Active mode**: client opens port 21; server *connects back* to the client's ephemeral port for data (breaks behind NAT).
  - **Passive mode** (PASV): client opens the data connection to the server (works through NAT/firewalls; default today).
  - Commands/responses are ASCII (USER, PASS, TYPE, PASV, PORT, RETR, STOR, QUIT; replies 200/230/550...). Plaintext credentials by default → **FTPS** (explicit/implicit TLS) fixes this.
- **SSH** (RFC 4251): client/server on port **22**; three sub-protocols — **transport** (host key + key exchange → encryption), **user authentication** (password, public key), **connection** (multiplexes channels: shell, port forwarding, SFTP, SCP). Public-key auth: client's `~/.ssh/id_ed25519.pub` authorized on server's `~/.ssh/authorized_keys`; `ssh-keygen`, `ssh-agent`, `AgentForwarding`.
- **SFTP** (RFC 9131): a *file protocol inside SSH* — one connection, encrypted, subcommands (get/put/ls/rm/rename/stat), streaming.
- **SCP** (RFC 9142): file copy over SSH using `scp` (deprecated-ish in favor of SFTP but ubiquitous).
- **Telnet** (RFC 854): plaintext virtual terminal (NVT), port 23. Today: legacy devices, debugging (raw TCP test), always inside trust boundaries.

## 3. When Is It Used?
- **FTP/FTPS**: legacy data exchange (file dumps, EDI), embedded/IoT device firmware, public file mirrors (legacy), some enterprise automation. Rare for new greenfield work.
- **SFTP/SCP**: the modern default for file transfer to servers (deploy, backups, uploads), CI/CD (rsync/scp to hosts), data exchange between businesses.
- **SSH**: every cloud VM, Kubernetes nodes, network gear (IOS/Netconf over SSH), git over SSH (git@github.com), tunneling (SSH -L/-R, SOCKS proxy), SFTP backend.
- **Telnet**: legacy routers/printers (serial-over-network), raw TCP protocol debugging (`telnet host port` to test SMTP/HTTP), embedded systems without SSH.
- **Related services**: rsync (efficient file sync, often over SSH), NFS (network file sharing, port 2049), SMB (Windows file sharing, 445), TFTP (trivial boot file transfer, UDP 69 — PXE).

## 4. Why Wasn't Another Approach Chosen?
- **Why two channels (control + data) in FTP?** To allow the control session to outlive/coordinate multiple data transfers and keep command state (dirs, modes) separate from bulk bytes. The cost: complexity, NAT problems (hence PASV), and firewall pain — a design later rejected by SFTP (one stream).
- **Why not just encrypt FTP?** Because FTP's dual-connection model is broken by firewalls/NATs, and even FTPS keeps the awkward dance. SFTP reuses SSH's single encrypted channel — simpler, works everywhere. "Why wasn't another approach chosen" → the industry *did* abandon FTP semantics for SFTP/SSH.
- **Why SSH instead of patching Telnet?** Telnet had no encryption and no forward-secret key exchange; retrofitting was worse than a new protocol. SSH (by Tatu Ylönen, 1995) was built fresh with host-key auth + per-session keys + perfect forward secrecy.
- **Why public-key auth over password?** Passwords are guessable/replayable; SSH keys are long random secrets. Key auth also enables agent-based single sign-on and automation (CI/CD without interactive passwords).
- **Why did FTP/SFTP/rsync coexist?** FTP = legacy + interoperability; SFTP = secure file over SSH (deploy, exchange); rsync = delta sync (only changed blocks) — each optimizes a different axis (compat, security, bandwidth).

## 5. Intuition
- **FTP** = a **file server with two doors**: one door for instructions (control, 21), another for the actual boxes moving (data). With PASV, you (the client) walk in and the warehouse worker carries boxes through *your* door — the modern mode that survives firewalls.
- **Telnet** = a **speaking tube with no walls**: anyone tapping the pipe hears every word — including the password. Fine in a trusted basement, terrifying on the Internet.
- **SSH** = the same tube but **soundproofed and door-locked with a signing ceremony**: each side proves identity (host key), they agree on a secret (DH), and everything is encrypted; your key is a special ID card, and `ssh-agent` is the trusted valet who holds it so you don't type it.
- **SFTP** = moving files through that locked, soundproofed tunnel — one pipe, everything inside.

## 6. Real-World Analogy
**The vault courier company**: Old FTP = you call the company's office (control line, 21), then their courier drives a truck (data line) to your address to drop/pick boxes — but the office and truck both transmit the cargo manifest *in plain view* (plaintext). Telnet = talking to the warehouse foreman through an uninsulated wall — every word leaks. SSH = the courier company switched to **sealed armored trucks** (encryption): the foreman (host) shows you a notarized ID (host key), you two quietly agree on a route+key (key exchange), and the truck (data) moves only inside the secured operation. SFTP = you send files *inside* the armored truck; SCP = a quick sealed-courier copy; rsync = a clever courier who only ships the *changed* pages.

## 7. Formal Definition
- **FTP** (RFC 959): a protocol for transferring files over TCP using a **control connection** (port 21, text commands `USER`, `PASS`, `CWD`, `PASV`, `RETR`, `STOR`) and a separate **data connection** (active: server connects back; passive: client connects). Authentication and data are plaintext; **FTPS** (RFC 4217) wraps it in TLS.
- **SSH** (RFC 4251-4254): a protocol for secure remote login and other network services over TCP port 22, composed of the **transport layer** (host authentication + key exchange → encryption, e.g., curve25519-sha256, aes128-gcm), the **authentication layer** (password, public-key, keyboard-interactive), and the **connection layer** (multiplexed channels). Provides confidentiality, integrity, and server (and optionally client) authentication.
- **SFTP** (RFC 9131): a secure file-transfer sub-protocol running *inside* SSH's encrypted channel, with its own command set (open/close/read/write/stat/opendir/remove/rename/realpath), supporting streaming and resume. Distinct from FTPS (which is FTP-over-TLS).
- **Telnet** (RFC 854): a plaintext remote-terminal protocol (Network Virtual Terminal), port 23, providing no encryption or authentication.

## 8. Example
FTP passive transfer (typical modern):
```
Client                          FTP Server (port 21)
  |----> USER alice             -> 331 Password required
  |----> PASS secret            -> 230 Logged in            (plaintext! visible)
  |----> PASV                   -> 227 Entering Passive Mode (192,168,1,5,200,5)
  |----> RETR report.pdf        -> 150 Opening data connection
  |<--- data connection (client connects to server port 51205) ----  (port = 200*256+5)
  |                             -> 226 Transfer complete
  |----> QUIT                   -> 221 Goodbye
```
SFTP (equivalent, over SSH):
```
Client --SSH(22)--> Server
  SSH transport: host key verify + curve25519 key exchange -> encrypted channel
  SSH auth: public key (or password, now encrypted)
  SFTP: OPEN "report.pdf" READ -> DATA blocks -> CLOSE   (all inside SSH, encrypted)
```
Telnet vs SSH command line:
```
$ telnet 192.168.1.5     # opens plaintext session; everything visible in tcpdump
$ ssh -i ~/.ssh/id_ed25519 alice@192.168.1.5   # encrypted, key-authenticated
```

## 9. Internal Working
1. **FTP control flow**: commands are 4-char verbs + args; replies are 3-digit with continuation `-`. Stateful: login, CWD (current dir), TYPE (ASCII/binary), mode. The data connection: active = server connects to the client's PASV-announced port; passive = client connects to server's announced port.
2. **FTP NAT problem**: active mode's server→client callback breaks NAT (no route back). PASV solves it (client initiates both). FTPS adds TLS on control (explicit AUTH TLS) and optionally data (PROT P).
3. **SSH transport**: client sends identification banner + key-exchange init → both compute a shared secret (ECDH, e.g., curve25519) → derive session keys → server proves identity by signing the exchange with its host key (host-key check: `known_hosts` stores the fingerprint; TOFU on first connect). All further traffic encrypted (AES-GCM/ChaCha20) + integrity (MAC/AEAD).
4. **SSH auth**: password (sent encrypted), **public key** (client signs a challenge with its private key; server verifies the public key in `authorized_keys`), or certificate/agent. `ssh-agent` holds keys in memory, offering signatures without exposing the private key (agent forwarding chains trust carefully).
5. **SSH connection layer**: multiple **channels** multiplexed over one transport: interactive shell, exec (single command), SFTP subsystem, forwarded TCP (port forwarding `-L/-R`), SOCKS (`-D`). This multiplexing is SSH's superpower vs Telnet's single stream.
6. **SFTP**: a binary protocol (not text like FTP) with packets: `SSH_FXP_INIT`, `OPEN`, `READ`, `WRITE`, `STAT`, `OPENDIR`, `READDIR`, `CLOSE`, `REMOVE`, `RENAME`. Server-side ops, streaming, and resumption (offset-based reads). It's a *secure file protocol*, not "FTP over SSH" in the packet sense.
7. **SCP**: legacy protocol (RFC 9142 standardizes it) using `scp` — simple copy over the SSH exec channel with a minimal protocol; superseded by SFTP for features, still common in scripts.
8. **Telnet internals**: NVT + option negotiation (IAC, DO/DONT/WILL/WONT) for echo, window size, line mode. Debugging uses: connect to arbitrary ports to speak raw protocols (e.g., `telnet host 80` → type an HTTP GET).

## 10. Time Complexity
- **FTP**: control O(1) per operation; data transfer O(file size) — same as any file copy. Two connections → firewall/NAT setup cost (the real overhead).
- **SSH handshake**: ~1 RTT for key exchange (server-auth keys) + ~1 RTT for user auth (public key with agent) → sub-second typical; crypto CPU per packet is negligible (AES-GCM at GB/s with AES-NI).
- **SFTP**: O(file size) transfer, O(chunks) round trips; per-chunk windowed streaming amortizes RTT. Resume = continue from offset (O(1) setup).
- **rsync over SSH**: delta algorithm makes transfer O(changed blocks) instead of O(whole file) — the reason it's used for large/backup syncs.

## 11. Advantages
- **FTP/FTPS**: universally understood, ASCII scripting, passive mode for NAT, mature tooling; FTPS adds TLS to a familiar protocol.
- **SSH**: encrypted + integrity, host-key auth, PFS (ephemeral DH), public-key + agent auth, channel multiplexing, tunneling (port forwarding, SOCKS), automation-friendly, ubiquitous.
- **SFTP**: one secure channel, streaming/resume, works through NAT/firewalls, integrated with SSH auth, no plaintext ever.
- **Telnet**: minimal footprint, useful raw-TCP debugging, legacy gear support.

## 12. Disadvantages
- **FTP**: plaintext credentials/data by default (sniffable), dual-connection NAT pain, no integrity checks, passive-mode server config complexity, firewalls hate it.
- **Telnet**: everything plaintext (passwords, commands) — unacceptable on any untrusted network; no host authentication.
- **SFTP/SCP**: slightly slower than raw FTP (crypto), needs SSH keys management, protocol negotiation overhead, SCP deprecated for features.
- **SSH**: key management burden, host-key TOFU trust model (MITM on first connect), agent-forwarding risks, corporate firewall familiarity, CPU cost on low-end devices.

## 13. Interview Questions
1. **Q: FTP vs SFTP vs FTPS — what's the difference?** A: FTP = plaintext file transfer (control 21 + data). FTPS = FTP over TLS (same model, encrypted). SFTP = a *file protocol inside SSH* (one encrypted connection, port 22). Different mechanisms entirely — SFTP is not "secure FTP."
2. **Q: Why does FTP need two connections?** A: A control connection (commands, port 21) plus a data connection (file bytes). The control session is stateful (login, cwd, mode); the data channel moves bulk. This split caused NAT/firewall pain → PASV was added.
3. **Q (tricky): Active vs passive FTP — which works through NAT and why?** A: Passive (PASV): the *client* initiates both connections (control then data to a server-announced port) — works through NAT/firewalls. Active: the *server* initiates the data connection back to the client — blocked by NAT (no inbound route) unless port-forwarded.
4. **Q: What does SSH provide that Telnet doesn't?** A: Encryption (confidentiality), integrity (no tampering), host authentication (verify the server), and user authentication (password/public key) — Telnet is plaintext with no auth. SSH also multiplexes channels and tunnels.
5. **Q: How does SSH public-key authentication work?** A: Client proves possession of the private key by signing a challenge; the server verifies against the public key in `authorized_keys`. The private key never leaves the client (with `ssh-agent`, it may never even be exposed to the session).
6. **Q (production): Why do you use `ssh -i` keys rather than passwords on servers?** A: Keys are long, unguessable, non-replayable, and support agent-based single sign-on and automation (CI/CD deploys with no interactive password). Passwords are brute-forceable and observable. Standard cloud practice: disable password auth, keys only.
7. **Q: What is SSH tunneling / port forwarding?** A: SSH multiplexes channels, so you can forward a local port to a remote service (`ssh -L 8080:db.internal:5432 user@bastion`) — encrypting and traversing NAT/firewalls. `-R` reverse, `-D` SOCKS proxy. It's the classic "secure tunnel" primitive.
8. **Q: What is the host-key / TOFU model in SSH?** A: On first connect, SSH saves the server's host-key fingerprint in `known_hosts` (Trust On First Use); on later connects it verifies the same key — a changed host key (MITM or server rebuild) triggers a warning. Better than nothing; cert-based SSH (RFC 4252) strengthens it.
9. **Q (scenario): You see `telnet` in a security scan. What's the risk and fix?** A: Plaintext — anyone on path reads credentials + commands (MITM). Fix: disable Telnet, enable SSH only, ensure legacy gear supports it (or wrap Telnet in an SSH tunnel at minimum).
10. **Q: What's the difference between SCP and SFTP?** A: Both run over SSH. SCP = simple copy (the classic `scp` protocol, now RFC 9142); SFTP = full-featured file protocol (list/stat/resume/rename/perms) with richer semantics. Prefer SFTP for new work; SCP remains in scripts/backups.
11. **Q: What is rsync and how is it more efficient than a plain copy?** A: rsync computes block checksums and transfers only *changed* blocks (delta algorithm) — O(changed) not O(whole). Usually runs over SSH (`rsync -avz -e ssh`). Ideal for backups, large file mirrors, deploys.
12. **Q (tricky): Is SFTP port 22 or a different port?** A: SFTP uses **port 22** (it runs inside SSH's connection layer). There's no separate SFTP port. FTP uses 21/20; FTPS uses 21 (control) + explicit TLS; some use 990 (implicit). Common gotcha.
13. **Q: What's the difference between TFTP and FTP?** A: TFTP = trivial, UDP-based (port 69), no auth, no directory listing — used only for bootstrapping (PXE, router firmware). FTP = TCP, auth, full file ops. Different niches, not versions of each other.
14. **Q (production): How would you securely automate file drops between two companies?** A: Prefer SFTP (public-key auth, one encrypted channel) over FTPS for simplicity; or MFT (managed file transfer) for compliance + audit; add IP allowlists, key rotation, and per-customer accounts. The "secure drop" pattern is usually SFTP or object storage (S3 presigned).
15. **Q: What are NFS and SMB and how do they differ from FTP/SFTP?** A: NFS (2049) and SMB (445) are *network file systems* — the OS mounts a remote share, reads/writes look local (stateless-ish block/file ops). FTP/SFTP are *transfer* protocols — you copy a file, not mount it. Different models: share vs copy.
16. **Q: Why does SSH still need to be patched even though it's "secure"?** A: "Secure" is a moving target: algorithm deprecation (old KEX, SHA-1, CBC modes), protocol bugs (Terrapin prefix truncation, CVE-2023-48795), and key mismanagement. Run current OpenSSH, disable legacy ciphers/KEX, rotate keys. Security protocols age.

## 14. Follow-Up Questions
1. **Q: What is "SSH agent forwarding" and why is it risky?** A: The agent forwards the *authentication request* (not the key) to intermediate hosts — but a root-compromised intermediate can use the agent while you're connected. Risk: privilege propagation. Alternative: `ProxyJump` (keys stay local) — the safer modern pattern.
2. **Q: What is the difference between ECDH and RSA in SSH?** A: ECDH (curve25519) = key *exchange* (agreement, ephemeral, PFS) — fast and forward-secret. RSA = *signature* (host/user auth, identity) — still widely used but longer keys needed. SSH pairs them: ECDH for the session, RSA/Ed25519 for identity.
3. **Q: What is "key-based" vs "certificate-based" SSH auth?** A: Public keys are shared manually (authorized_keys, TOFU). SSH certificates (RFC 4252 CA-signed) let a CA sign host/user keys — central revocation and expiry, no manual per-host entries. Used at scale in datacenters.
4. **Q: How do you handle SSH key rotation at scale?** A: Central inventory, short-lived certs, automated key scanning (e.g., GitHub's `ssh-auditor`), disallow reuse, agent-based central sign-on, and regular audits. Rotation discipline = security hygiene.
5. **Q: What is "Mosh" and why does it exist?** A: Mobile shell — UDP-based SSH alternative that survives IP changes and network blips (stateful predictive echo) for flaky connections. SSH's TCP sessions break on network change; Mosh keeps the session alive.

## 15. Coding Example
```bash
# Everyday secure operations (the interview-relevant tooling)
$ ssh-keygen -t ed25519 -C "work@laptop"          # modern key type (Ed25519)
$ ssh-copy-id alice@server                        # install public key
$ ssh alice@server "uptime"                        # run a command (encrypted)
$ ssh -L 8080:db.internal:5432 alice@bastion       # tunnel: local 8080 -> db.internal:5432
$ scp file.txt alice@server:/data/                 # secure copy (legacy)
$ sftp alice@server <<'EOF'                        # interactive/scripted SFTP
  put report.pdf
  get backup.tar
  quit
EOF
$ rsync -avz -e ssh ./build/ alice@server:/var/www/  # delta sync over SSH (deploy)
```
```python
# paramiko: scripted SFTP over SSH (the automation layer)
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("server.example.com", username="alice", key_filename="~/.ssh/id_ed25519")

sftp = ssh.open_sftp()                      # SFTP subsystem over the SSH channel
sftp.put("report.pdf", "/data/report.pdf")  # encrypted transfer
print(sftp.stat("/data/report.pdf").st_size)
sftp.close(); ssh.close()
```
```
# Prove the FTP plaintext problem (why everyone moved to SFTP/SSH)
$ tcpdump -nn -A 'tcp port 21'     # FTP control: see USER/PASS in clear text!
# ....USER alice....PASS secret...   <- visible to anyone on the path
$ tcpdump -nn 'tcp port 22'         # SSH: only binary ciphertext, headers only
```

## 16. Industry Usage
- **Every cloud**: AWS/Azure/GCP VMs are managed over SSH (port 22); `scp`/`sftp` for deploys; SSH tunnels to private resources (`aws ssm` now often replaces it for serverless management).
- **Git/GitHub**: `git@github.com` = SSH auth; the SSH protocol powers distributed version control transport.
- **CI/CD**: Jenkins/GitHub Actions deploy via SSH + rsync/scp; Ansible manages servers over SSH (port 22) by default — automation depends on key auth.
- **Enterprise file transfer**: SFTP/MFT (B2B drops, banking files, healthcare EDI) — compliance requires encryption + audit; SFTP is the workhorse.
- **Network gear**: Cisco/Juniper devices accept SSH (IOS management) and deprecated Telnet; Netconf/SSH is the modern config transport. IoT/embedded: FTPS or SSH for firmware updates.

## 17. References
- RFC 959 — FTP: https://www.rfc-editor.org/rfc/rfc959
- RFC 4217 — FTPS (FTP over TLS): https://www.rfc-editor.org/rfc/rfc4217
- RFC 4251-4254 — SSH: https://www.rfc-editor.org/rfc/rfc4251
- RFC 9131 — SFTP: https://www.rfc-editor.org/rfc/rfc9131
- RFC 9142 — SCP: https://www.rfc-editor.org/rfc/rfc9142
- RFC 854 — Telnet: https://www.rfc-editor.org/rfc/rfc854
- RFC 1350 — TFTP: https://www.rfc-editor.org/rfc/rfc1350
- Kurose & Ross, *Computer Networking*, 8th ed., Ch. 2 (Application layer).

## 18. Cheat Sheet
- FTP: control 21 + data (PASV for NAT), plaintext → FTPS adds TLS.
- SFTP = file protocol *inside* SSH (port 22). SCP = simple copy over SSH.
- SSH: transport (host key + ECDH) → auth (public key/password) → connection (channels).
- Telnet = plaintext (port 23) — never on untrusted networks.
- SSH tunnels: -L local, -R remote, -D SOCKS.
- Public-key auth: id_ed25519.pub → authorized_keys; ssh-agent holds keys.
- rsync: delta sync (changed blocks) over SSH.
- NFS (2049) / SMB (445) = mount; FTP/SFTP = copy.
- TFTP (UDP 69) = bootstrapping only.
- Agent forwarding risk → use ProxyJump.

## 19. Quiz
1. FTP control port: a) 22 b) 21 c) 25 d) 69 → **b**
2. SFTP runs over: a) port 21 b) SSH (22) c) UDP 69 d) TLS 443 → **b**
3. Which is encrypted? a) Telnet b) FTP c) SSH d) TFTP → **c**
4. Passive FTP: a) server connects back b) client connects data to server c) no data d) UDP → **b**
5. SSH public-key auth proves: a) password b) possession of private key c) IP d) MAC → **b**
6. `ssh -L 8080:db:5432` creates: a) a file transfer b) a local forward tunnel c) a SOCKS proxy d) a VPN → **b**
7. Which protocol is for mounting (not copying)? a) FTP b) SMB c) SFTP d) SCP → **b**
8. SCP vs SFTP: a) same b) SFTP richer file ops c) SCP encrypted, SFTP not d) SFTP is FTP-over-TLS → **b**
9. TFTP is used for: a) big file transfers b) PXE/bootstrapping c) email d) DNS → **b**
10. Agent forwarding risk: a) slower b) compromise of intermediate host can use your agent c) breaks keys d) no encryption → **b**

## 20. Flashcards
- **Q: FTP vs SFTP vs FTPS?** → **A:** FTP plaintext; FTPS = FTP-over-TLS; SFTP = file protocol inside SSH.
- **Q: Why PASV?** → **A:** Client initiates the data connection → works through NAT/firewalls.
- **Q: SSH layers?** → **A:** Transport (host key + KEX), Auth (public key/password), Connection (channels).
- **Q: Telnet problem?** → **A:** Everything plaintext (no encryption/auth) — replaced by SSH.
- **Q: SSH tunnel -L?** → **A:** Local port → remote service, encrypted.
- **Q: rsync advantage?** → **A:** Delta sync — transfers only changed blocks.
- **Q: NFS/SMB vs FTP?** → **A:** Mount (shared FS) vs copy (transfer).

## 21. Revision
FTP (21 control + data, PASV for NAT) is plaintext → FTPS adds TLS; SFTP runs file ops *inside* SSH (port 22); SCP is simple copy over SSH; Telnet (23) is plaintext and obsolete for security. SSH = transport (host key + ECDH key exchange, PFS) → auth (public key via authorized_keys / ssh-agent) → connection layer (channels, tunnels -L/-R/-D). Public-key auth = sign a challenge. rsync does delta sync over SSH. NFS/SMB mount, FTP/SFTP copy. TFTP (UDP 69) is for bootstrapping. Prefer SSH/SFTP everywhere; Telnet/FTP only in trust boundaries.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "FTP vs SFTP vs FTPS?" | 2 How It Works / 13 Q&A |
| "Why does FTP need two connections?" | 9 Internal Working / 13 Q&A |
| "How does SSH public-key auth work?" | 9 Internal Working / 13 Q&A |
| "SSH vs Telnet?" | 13 Q&A / 4 Why Another Approach |
| "What is SSH tunneling?" | 13 Q&A / 9 Internal Working |
| "Why disable Telnet/passwords?" | 13 Q&A / 16 Industry Usage |
| "SCP vs SFTP?" | 13 Q&A / 7 Formal Definition |
| "How does rsync beat a copy?" | 13 Q&A / 10 Time Complexity |
