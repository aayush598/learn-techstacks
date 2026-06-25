# Access Control

## Access Control Lists (ACL)
- Per-object list: `(user, rights)` entries
- When access requested: search list for matching user
- **Unix permissions**: 9-bit mode (`rwxr-xr-x`)
  - Owner, Group, Other — each with read(4), write(2), execute(1)
- Extended ACLs (POSIX ACL): multiple named users/groups

## Special Permissions (Unix)
- **setuid** (`chmod u+s`): execute as file owner (e.g., `/bin/passwd`)
- **setgid** (`chmod g+s`): execute as file group
- **Sticky bit** (`chmod +t`): only owner can delete (e.g., `/tmp`)

## Capability Lists
- Per-domain list: `(object, rights)` pairs
- Process presents capability → system verifies → grants access
- **POSIX capabilities**: fine-grained root privileges (CAP_NET_BIND_SERVICE, CAP_SYS_ADMIN)
- Capabilities are **protected** (cannot be forged)

## ACL vs Capability Comparison
| Feature | ACL | Capability |
|---------|-----|------------|
| Granularity | Per object | Per domain |
| Revocation | Easy (edit list) | Hard (track copies) |
| Delegation | Manual | Process passes capability |
| Performance | Search O(n) per access | Direct reference |
| Paradigm | Who can access this? | What can this access? |

## RBAC (Role-Based Access Control)
- **Roles** instead of individual users
- Users assigned to roles, roles have permissions
- **Role hierarchy**: senior roles inherit junior permissions
- Benefits: simplifies administration, follows least privilege
- **NIST standard**: RBAC has 4 model levels (Flat, Hierarchical, Constrained, Symmetric)
