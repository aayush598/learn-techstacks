# Session Management

## 1. Overview

Session management handles user state across multiple requests in the recommendation
system. Sessions enable personalization continuity, cross-device experiences, and
secure user state management. This document covers session creation, storage, expiry,
invalidation, cross-device handling, and security measures for production recommendation
systems.

### 1.1 Session vs Token-Based Auth

| Aspect | Session (Server-Side) | JWT (Stateless) |
|---|---|---|
| State location | Server (Redis) | Client (token) |
| Revocation | Instant (delete session) | Difficult (blacklist) |
| Scalability | Requires shared storage | Horizontally scalable |
| Server memory | Stores session data | Token contains claims |
| Use case | Web apps, personalization | APIs, microservices |

### 1.2 Session Architecture

```
Client ←→ API Gateway ←→ Session Service ←→ Redis Cluster
                        ↕
                   Recommendation Engine
                        ↕
                   Feature Store / Model Registry
```

---

## 2. Session Creation

### 2.1 Session Lifecycle

```
User Login → Create Session → Store in Redis → Set Cookie/Header → Return to Client
    ↓                                                                      ↓
  Verify                                                       Session ID sent
  credentials                                                   with each request
```

### 2.2 Session Data Structure

```json
{
  "session_id": "sess_a1b2c3d4e5f6g7h8",
  "user_id": "usr_x9y8z7w6v5u4",
  "created_at": "2026-01-15T10:30:00Z",
  "last_accessed": "2026-01-15T14:45:00Z",
  "expires_at": "2026-01-15T22:30:00Z",
  "device_info": {
    "type": "mobile",
    "os": "iOS 18",
    "browser": "Safari"
  },
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "permissions": ["read:recommendations", "write:interactions"],
  "experiment_groups": ["exp_new_algo_v2"],
  "personalization_state": {
    "last_recommendations": ["item_1", "item_2"],
    "interaction_count": 47,
    "session_relevance_score": 0.85
  }
}
```

### 2.3 Session Creation Triggers

| Trigger | Session Type | Expiry | Persistence |
|---|---|---|---|
| Email/password login | Full session | 24 hours | Persistent |
| OAuth login | Full session | 24 hours | Persistent |
| Social login | Full session | 24 hours | Persistent |
| Anonymous browse | Ephemeral session | 30 minutes | Not persistent |
| API key access | Service session | 1 hour | Not persistent |

### 2.4 Session ID Generation

- **Length**: 32 bytes (256 bits) of randomness
- **Format**: `sess_` + hex-encoded random bytes
- **Generation**: CSPRNG (Cryptographically Secure PRNG)
- **Uniqueness**: Collision probability < 2^-128
- **No sequential IDs**: Prevent session ID prediction

---

## 3. Session Storage

### 3.1 Redis Session Store

| Property | Configuration |
|---|---|
| Data structure | Hash (session_id → session data) |
| Serialization | JSON with compression |
| Memory policy | volatile-lru (evict expired sessions first) |
| Persistence | RDB snapshots + AOF for durability |
| Replication | Master-replica with automatic failover |
| Cluster mode | Redis Cluster with hash slot distribution |

### 3.2 Session Storage Operations

| Operation | Command | Latency |
|---|---|---|
| Create session | HSET with TTL | < 1ms |
| Read session | HGETALL | < 1ms |
| Update session | HSET (specific fields) | < 1ms |
| Delete session | DEL | < 1ms |
| Extend session | EXPIRE | < 1ms |
| List user sessions | SCAN with pattern | < 5ms |

### 3.3 Session Data Partitioning

```
Redis Cluster Session Distribution:
├── Shard 1: Sessions a-f* (hash slot 0-2730)
├── Shard 2: Sessions g-m* (hash slot 2731-5460)
├── Shard 3: Sessions n-s* (hash slot 5461-8191)
└── Shard 4: Sessions t-z* (hash slot 8192-16383)
```

### 3.4 Session Storage Size Management

- **Session size limit**: Max 4KB per session
- **Large data**: Store references, not full data (recommendation history → separate key)
- **Compression**: Enable gzip for sessions > 1KB
- **Cleanup**: Expired sessions automatically removed by Redis TTL

---

## 4. Session Expiry

### 4.1 Expiry Policies

| Session Type | Absolute Timeout | Idle Timeout | Sliding Window |
|---|---|---|---|
| Web session | 24 hours | 30 minutes | Yes |
| Mobile session | 7 days | 24 hours | Yes |
| API session | 1 hour | 15 minutes | No |
| Admin session | 8 hours | 30 minutes | Yes |
| Anonymous session | 30 minutes | 30 minutes | No |

### 4.2 Sliding Window Expiry

Extend session expiry on each valid request:

```
Initial: expires_at = now + idle_timeout
On each request: expires_at = now + idle_timeout (if < absolute_timeout)
Never: expires_at > created_at + absolute_timeout
```

### 4.3 Expiry Handling

**Client-side expiry:**
- JavaScript timer warns user before session expires
- Automatic refresh request before expiry
- Graceful redirect to login on expiry
- Preserve user's last page/action for post-login redirect

**Server-side expiry:**
- Redis TTL automatically removes expired sessions
- Expired session access returns null (treated as new session)
- No error logged for normal session expiry (only for anomalies)
- Session expiry metrics tracked for monitoring

---

## 5. Session Invalidation

### 5.1 Invalidation Scenarios

| Scenario | Scope | Method | SLA |
|---|---|---|---|
| User logout | Current session | Delete session from Redis | Immediate |
| Change password | All user sessions | Delete all user sessions | Immediate |
| Account compromise | All user sessions | Delete all + revoke tokens | Immediate |
| Admin action | Specific session | Delete specific session | Immediate |
| Security policy | All sessions | Flush session store | < 5 minutes |

### 5.2 Cross-Device Session Invalidation

When a user changes password, invalidate all sessions across devices:

```
Password Change → Find All User Sessions → Delete from Redis → Notify Devices
      ↓                    ↓                     ↓                 ↓
  Verify old         SCAN user:*           DEL each session    Push notification
  password           pattern               ID                  to mobile apps
```

### 5.3 Session Invalidation Propagation

- **Immediate deletion**: Session removed from Redis immediately
- **API gateway cache**: Gateway invalidates session cache within 1 second
- **Client notification**: WebSocket/push notification to active clients
- **Cookie clearing**: Client instructed to clear session cookie

---

## 6. Cross-Device Sessions

### 6.1 Cross-Device Personalization

Recommendation systems benefit from cross-device session awareness:

| Feature | Implementation | Privacy Consideration |
|---|---|---|
| Continue on other device | Share session via user account | User must be logged in |
| Cross-device history | Merge interaction history | Consent required |
| Device linking | Associate devices with user | Clear linking UI |
| Cross-device recommendations | Unified user profile | Respect privacy settings |

### 6.2 Device Linking

```
Device A (logged in) → Generate linking code → User enters on Device B
                                                      ↓
                                              Device B linked to user
                                              Shared personalization active
```

### 6.3 Cross-Device Session Management

- **Max devices**: Limit concurrent sessions per user (e.g., 5 devices)
- **Device priority**: Prioritize most recent/active device for features
- **Session limits**: When limit exceeded, oldest session invalidated
- **Device management UI**: User can view and manage linked devices

---

## 7. Session Security

### 7.1 Anti-Hijacking Measures

| Measure | Implementation | Purpose |
|---|---|---|
| IP binding | Store session IP, validate on access | Prevent session theft |
| User agent binding | Store UA string, validate on access | Prevent session transfer |
| Token rotation | Rotate session ID on privilege change | Limit exposure window |
| Concurrent session limit | Max N sessions per user | Reduce attack surface |
| Anomaly detection | Flag unusual access patterns | Detect hijacked sessions |

### 7.2 Session Fixation Prevention

Prevent attackers from fixing a session ID before login:

1. **Generate new session ID on login**: Never reuse pre-login session
2. **Invalidate old session**: Delete any pre-login session after authentication
3. **Regenerate on privilege change**: New session ID when role changes
4. **Server-side session creation**: Session ID always generated server-side

### 7.3 Session Cookie Security

| Property | Setting | Rationale |
|---|---|---|
| HttpOnly | true | Prevent JavaScript access |
| Secure | true | HTTPS only transmission |
| SameSite | Strict | Prevent CSRF attacks |
| Domain | .example.com | Subdomain scope |
| Path | / | Application scope |
| Max-Age | 86400 (24h) | Session lifetime |

### 7.4 Session Security Monitoring

Track and alert on suspicious session activity:

- **Multiple IP access**: Same session from different IPs in short timeframe
- **Impossible travel**: Session accessed from geographically distant locations
- **Concurrent sessions**: Excessive simultaneous sessions per user
- **Brute force**: Many failed session creation attempts
- **Session fixation**: Pre-login session ID reused after authentication

### 7.5 Session Security Best Practices

1. **Encrypt session data at rest** in Redis
2. **Use HTTPS everywhere** for session transmission
3. **Implement session timeout** with both idle and absolute limits
4. **Log session events** for audit trail
5. **Rate limit session creation** to prevent abuse
6. **Validate session on every request** (not just at authentication)
7. **Implement session revocation** with propagation guarantees
8. **Regular security audits** of session management code
