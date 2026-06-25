# Security Threats

## CIA Triad
- **Confidentiality**: only authorized users can access data
- **Integrity**: data is accurate and hasn't been tampered with
- **Availability**: system/data accessible when needed

## Types of Threats
| Threat | Description |
|--------|-------------|
| **Virus** | Attaches to executable, spreads when run |
| **Worm** | Self-replicating, spreads via network (no host needed) |
| **Trojan** | Disguised as legitimate software |
| **Ransomware** | Encrypts files, demands ransom (e.g., WannaCry) |
| **Rootkit** | Hides in kernel/gaining root access, evades detection |
| **DoS/DDoS** | Overwhelms resources to deny service |

## Buffer Overflow
- Overwrite return address on stack → hijack control flow
- **Stack smashing**: write beyond buffer bounds
- Mitigations:
  - **ASLR** (Address Space Layout Randomization): randomizes memory addresses
  - **NX bit** (No-Execute): marks stack as non-executable
  - **Stack canaries**: insert guard value before return address (GCC's `-fstack-protector`)
  - Control-Flow Integrity (CFI)

## Other Attacks
- **MITM (Man-in-the-Middle)**: attacker intercepts communication
- **Privilege escalation**: gaining higher access (vertical/horizontal)
- **Side-channel**: infer data from timing, power, cache behavior
- **Spectre/Meltdown**: speculative execution reads privileged memory
- **SQL Injection**, **XSS**, **CSRF** (web-focused)
