# Access Matrix

## Protection Model
- **Protection domain**: set of (object, rights) pairs
- An object can be a file, device, memory segment, etc.
- Rights: read, write, execute, delete, own

## Access Matrix Structure
- **Rows**: domains (users/processes)
- **Columns**: objects (files, devices, etc.)
- **Cells**: access rights granted

| Domain | File A | File B | Printer |
|--------|--------|--------|---------|
| User A | read, write | read | -- |
| User B | read | write | print |
| Root | read, write, own | read, write, own | print |

## Domain Switching
- Processes can switch between domains
- Used during system calls (user → kernel mode)
- Setuid/setgid: temporarily change user identity

## Implementation Approaches
| Method | Structure | Lookup |
|--------|-----------|--------|
| **Global table** | Single large matrix | Domain + Object → rights |
| **ACL** (per-object) | List per object | Object → [(user, rights)] |
| **Capability list** | List per domain | Domain → [(object, rights)] |
| **Lock-key** | Object has locks, domain has keys | Match lock to key |

## Revocation
- **Immediate vs Delayed**: rights removed instantly vs at next check
- **Selective vs General**: specific user vs all users
- **Capability revocation**: harder than ACL (must track all copies)
- ACL revocation: simply edit the list entry
