# Naming & Caching in DFS

## Location Transparency
- **File name does not encode physical location**
- `/home/user/file.txt` vs `nfs://server01:/export/home/user/file.txt`
- Levels:
  - **Location transparency**: name unchanged when file moves
  - **Location independence**: name does not change even if file moves to different server

## Naming Mechanisms
- **DNS**: maps hostnames to IP addresses (hierarchical: `.com → google → www`)
- **URLs**: `scheme://host:port/path` (HTTP, NFS: `nfs://server/export/path`)
- **Paths**: absolute (`/home/user/f`) or relative (`./f`)
- **Symbolic links**: shortcuts to other files (can cross filesystem boundaries)

## Caching in DFS
- **Client-side cache**: stores recently accessed file data/attributes
- Reduces network traffic, improves performance
- Cache unit: **blocks** (NFS) vs **whole file** (AFS)

## Cache Consistency
| Strategy | How it works | Used by |
|----------|-------------|---------|
| **Check-on-access** | Validate cache before each read | NFS (v3) |
| **Callback** | Server notifies client on modification | AFS |
| **TTL** | Cache expires after fixed time | DNS |
| **Lease** | Server grants temporary cache permission | NFSv4 |

## Stateful vs Stateless Servers
| Aspect | Stateful | Stateless |
|--------|----------|-----------|
| **Performance** | Faster (cached state) | Slower (re-query each time) |
| **Crash recovery** | Must reconstruct state | Client retries, no state lost |
| **Memory** | Server uses memory per client | Minimal server memory |
| **Example** | AFS, NFSv4 | NFSv3 |

## Naming Services
- **Sun NIS** (Network Information Service): maps name → attributes centrally
- **LDAP** (Lightweight Directory Access Protocol): hierarchical directory, X.500-based
- **DNS**: distributed, hierarchical, most widely used
